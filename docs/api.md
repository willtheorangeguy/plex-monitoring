# API

Plex -> upstream exporter -> sanitizer that drops or aggregates session identity labels -> authenticated /metrics -> Prometheus -> Grafana.

## Interfaces

- `/metrics` requires the bearer token configured in the deployment. `/healthz` reports collector health.

## Prometheus scrape reference

See [examples/prometheus-scrape.yml](https://github.com/willtheorangeguy/plex-monitoring/blob/HEAD/examples/prometheus-scrape.yml) for the target, job name and authorization settings.

## Privacy transformations

The sanitizer aggregates upstream `plex_plays_active`, `plex_session_bandwidth_kbps` and `plex_session_bitrate_kbps` by their approved bounded labels. It drops `plex_play_seconds_total` and converts `plex_library_duration_milliseconds` to `plex_library_duration_seconds`. It emits `plex_sanitized_sessions_active`, stream and transcode breakdowns, and aggregate bandwidth. See [the sanitizer source](https://github.com/willtheorangeguy/plex-monitoring/blob/HEAD/sanitizer/src/plex_metrics_sanitizer.py) for its exact label rules.

`plex_sanitizer_up`, `plex_sanitizer_failures_total` and `plex_sanitizer_fetch_duration_seconds` report relay health. `/healthz` returns an unhealthy response after an upstream fetch or sanitization failure; a successful `/metrics` HTTP response can still contain only self metrics when the upstream request fails.
