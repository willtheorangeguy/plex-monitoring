#!/usr/bin/env python3
"""Authenticated, privacy-preserving relay for cplieger/plex-exporter."""

from __future__ import annotations

import collections
import hmac
import logging
import os
import re
import signal
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any


VERSION = "1.0.0"
AGGREGATIONS = {
    "plex_plays_active": ("stream_type", "transcode_type", "media_type", "location", "local"),
    "plex_session_bandwidth_kbps": ("location",),
    "plex_session_bitrate_kbps": ("location",),
}
DROP_FAMILIES = {"plex_play_seconds_total"}
NORMALIZE_FAMILIES = {
    "plex_library_duration_milliseconds": ("plex_library_duration_seconds", 0.001),
}
LABEL_RE = re.compile(r'([A-Za-z_][A-Za-z0-9_]*)="((?:\\.|[^"\\])*)"')
SAMPLE_RE = re.compile(
    r"^([A-Za-z_:][A-Za-z0-9_:]*)(?:\{(.*)\})?\s+([^\s]+)(?:\s+.*)?$"
)


def _escape_label(value: str) -> str:
    return value.replace("\\", "\\\\").replace("\n", "\\n").replace('"', '\\"')


def _unescape_label(value: str) -> str:
    return value.replace("\\n", "\n").replace('\\"', '"').replace("\\\\", "\\")


def _comment_family(line: str) -> str:
    fields = line.split()
    if len(fields) >= 3 and fields[0] == "#" and fields[1] in ("HELP", "TYPE", "UNIT"):
        return fields[2]
    return ""


def sanitize_metrics(text: str) -> str:
    """Keep server/library metrics and exactly aggregate privacy-sensitive sessions."""
    kept: list[str] = []
    aggregates: collections.defaultdict[
        tuple[str, tuple[tuple[str, str], ...]], float
    ] = collections.defaultdict(float)
    session_total = 0.0
    bandwidth_total = 0.0
    stream_types: collections.Counter[str] = collections.Counter()
    transcode_types: collections.Counter[str] = collections.Counter()

    for line in text.splitlines():
        if not line or line.strip() == "# EOF":
            continue
        if line.startswith("#"):
            family = _comment_family(line)
            if family in DROP_FAMILIES:
                continue
            if family in NORMALIZE_FAMILIES:
                normalized, _scale = NORMALIZE_FAMILIES[family]
                if line.startswith("# HELP "):
                    kept.append(
                        f"# HELP {normalized} Total duration of all items in the Plex library in seconds."
                    )
                elif line.startswith("# TYPE "):
                    kept.append(f"# TYPE {normalized} gauge")
                continue
            kept.append(line)
            continue

        match = SAMPLE_RE.match(line)
        if not match:
            raise RuntimeError("Unable to parse upstream Plex metric exposition")
        metric_name, label_text, value_text = match.groups()
        if metric_name in DROP_FAMILIES:
            continue
        if metric_name in NORMALIZE_FAMILIES:
            normalized, scale = NORMALIZE_FAMILIES[metric_name]
            labels = "{" + label_text + "}" if label_text is not None else ""
            kept.append(f"{normalized}{labels} {float(value_text) * scale:g}")
            continue
        if metric_name not in AGGREGATIONS:
            kept.append(line)
            continue

        labels = {
            key: _unescape_label(value)
            for key, value in LABEL_RE.findall(label_text or "")
        }
        required = AGGREGATIONS[metric_name]
        missing = [key for key in required if key not in labels]
        if missing:
            raise RuntimeError(
                f"Upstream {metric_name} is missing required labels: {','.join(missing)}"
            )
        safe_labels = tuple(sorted((key, labels[key]) for key in required))
        value = float(value_text)
        aggregates[(metric_name, safe_labels)] += value
        if metric_name == "plex_plays_active":
            session_total += value
            stream_types[labels["stream_type"]] += value
            transcode_types[labels["transcode_type"]] += value
        elif metric_name == "plex_session_bandwidth_kbps":
            bandwidth_total += value

    for (metric_name, labels), value in sorted(aggregates.items()):
        rendered = ",".join(
            f'{key}="{_escape_label(label)}"' for key, label in labels
        )
        kept.append(f"{metric_name}{{{rendered}}} {value:g}")

    kept.extend(
        [
            "# HELP plex_sanitized_sessions_active Active Plex sessions observed by the upstream exporter.",
            "# TYPE plex_sanitized_sessions_active gauge",
            f"plex_sanitized_sessions_active {session_total:g}",
            "# HELP plex_sanitized_sessions_by_stream_type Active Plex sessions by bounded playback decision.",
            "# TYPE plex_sanitized_sessions_by_stream_type gauge",
        ]
    )
    for stream_type in ("directplay", "copy", "transcode"):
        kept.append(
            f'plex_sanitized_sessions_by_stream_type{{stream_type="{stream_type}"}} '
            f"{stream_types[stream_type]:g}"
        )
    kept.extend(
        [
            "# HELP plex_sanitized_sessions_by_transcode_type Active Plex sessions by bounded transcode type.",
            "# TYPE plex_sanitized_sessions_by_transcode_type gauge",
        ]
    )
    for transcode_type in ("none", "video", "audio", "both"):
        kept.append(
            f'plex_sanitized_sessions_by_transcode_type{{transcode_type="{transcode_type}"}} '
            f"{transcode_types[transcode_type]:g}"
        )
    kept.extend(
        [
            "# HELP plex_sanitized_session_bandwidth_kbps Aggregate bandwidth of active Plex sessions in kilobits per second.",
            "# TYPE plex_sanitized_session_bandwidth_kbps gauge",
            f"plex_sanitized_session_bandwidth_kbps {bandwidth_total:g}",
        ]
    )
    return "\n".join(kept).rstrip() + "\n"


def render_self_metrics(up: float, failures: int, duration: float) -> str:
    return (
        "# HELP plex_sanitizer_build_info Plex metrics sanitizer build information.\n"
        "# TYPE plex_sanitizer_build_info gauge\n"
        f'plex_sanitizer_build_info{{version="{VERSION}"}} 1\n'
        "# HELP plex_sanitizer_up Whether the most recent upstream fetch and sanitization succeeded.\n"
        "# TYPE plex_sanitizer_up gauge\n"
        f"plex_sanitizer_up {up:g}\n"
        "# HELP plex_sanitizer_failures_total Upstream fetch or sanitization failures since start.\n"
        "# TYPE plex_sanitizer_failures_total counter\n"
        f"plex_sanitizer_failures_total {failures}\n"
        "# HELP plex_sanitizer_fetch_duration_seconds Duration of the most recent upstream fetch and sanitization.\n"
        "# TYPE plex_sanitizer_fetch_duration_seconds gauge\n"
        f"plex_sanitizer_fetch_duration_seconds {duration:g}\n"
    )


class Relay:
    def __init__(self, url: str, timeout: float) -> None:
        self.url = url
        self.timeout = timeout
        self.lock = threading.Lock()
        self.up = 0.0
        self.failures = 0
        self.duration = 0.0
        self.last_error = "not fetched yet"

    def fetch(self) -> str:
        started = time.monotonic()
        try:
            request = urllib.request.Request(
                self.url, headers={"User-Agent": f"plex-metrics-sanitizer/{VERSION}"}
            )
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                if response.status != 200:
                    raise RuntimeError(f"upstream returned HTTP {response.status}")
                raw = response.read().decode("utf-8")
            if "plex_server_info" not in raw:
                raise RuntimeError("upstream response did not contain Plex metrics")
            sanitized = sanitize_metrics(raw)
        except Exception as exc:
            duration = time.monotonic() - started
            with self.lock:
                self.up = 0.0
                self.failures += 1
                self.duration = duration
                self.last_error = str(exc)
                self_metrics = render_self_metrics(self.up, self.failures, self.duration)
            logging.error("Plex metrics relay failed: %s", exc)
            return self_metrics

        duration = time.monotonic() - started
        with self.lock:
            self.up = 1.0
            self.duration = duration
            self.last_error = ""
            self_metrics = render_self_metrics(self.up, self.failures, self.duration)
        return self_metrics + sanitized

    def health(self) -> tuple[bool, str]:
        with self.lock:
            return self.up == 1.0, self.last_error


def read_secret(path: str) -> str:
    with open(path, encoding="utf-8") as secret_file:
        value = secret_file.read().strip()
    if not value:
        raise RuntimeError(f"Secret file is empty: {path}")
    return value


def make_handler(relay: Relay, bearer_token: str):
    class Handler(BaseHTTPRequestHandler):
        server_version = "plex-metrics-sanitizer/" + VERSION

        def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
            path = urllib.parse.urlsplit(self.path).path
            if path == "/healthz":
                healthy, error = relay.health()
                payload = b"ok\n" if healthy else ("unhealthy: " + error + "\n").encode()
                self.send_response(200 if healthy else 503)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)
                return
            if path != "/metrics":
                self.send_error(404)
                return
            if not hmac.compare_digest(
                self.headers.get("Authorization", ""), "Bearer " + bearer_token
            ):
                payload = b"unauthorized\n"
                self.send_response(401)
                self.send_header("WWW-Authenticate", "Bearer")
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)
                return
            payload = relay.fetch().encode()
            self.send_response(200)
            self.send_header(
                "Content-Type", "text/plain; version=0.0.4; charset=utf-8"
            )
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def log_message(self, fmt: str, *args: Any) -> None:
            logging.info("HTTP %s - %s", self.address_string(), fmt % args)

    return Handler


def main() -> None:
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO"),
        format="%(asctime)s %(levelname)s %(message)s",
    )
    upstream_url = os.getenv("UPSTREAM_URL", "http://plex-exporter:9594/metrics")
    timeout = max(1.0, float(os.getenv("UPSTREAM_TIMEOUT_SECONDS", "15")))
    bearer_token = read_secret(
        os.getenv("EXPORTER_BEARER_TOKEN_FILE", "/run/secrets/exporter_bearer_token")
    )
    address = os.getenv("LISTEN_ADDRESS", "0.0.0.0")
    port = int(os.getenv("LISTEN_PORT", "9594"))

    relay = Relay(upstream_url, timeout)
    relay.fetch()
    server = ThreadingHTTPServer((address, port), make_handler(relay, bearer_token))

    def stop_server(_signum: int, _frame: Any) -> None:
        threading.Thread(target=server.shutdown, daemon=True).start()

    signal.signal(signal.SIGTERM, stop_server)
    signal.signal(signal.SIGINT, stop_server)
    logging.info("Listening on %s:%d and relaying %s", address, port, upstream_url)
    try:
        server.serve_forever()
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
