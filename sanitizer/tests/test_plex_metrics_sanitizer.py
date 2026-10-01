import pathlib
import sys
import unittest


sys.path.insert(0, str(pathlib.Path(__file__).parents[1] / "src"))

from plex_metrics_sanitizer import sanitize_metrics  # noqa: E402


class PlexMetricsSanitizerTests(unittest.TestCase):
    def test_session_metrics_are_aggregated_without_identity_labels(self):
        raw = """# HELP plex_server_info Server information
# TYPE plex_server_info gauge
plex_server_info{server="elfhame",server_id="abc",version="1.2"} 1
# HELP plex_plays_active Active plays
# TYPE plex_plays_active gauge
plex_plays_active{server="elfhame",title="Movie A",user="alice",session="one",device="TV",stream_type="directplay",transcode_type="none",media_type="movie",location="lan",local="true"} 1
plex_plays_active{server="elfhame",title="Movie B",user="bob",session="two",device="Web",stream_type="directplay",transcode_type="none",media_type="movie",location="lan",local="true"} 1
# HELP plex_session_bandwidth_kbps Bandwidth
# TYPE plex_session_bandwidth_kbps gauge
plex_session_bandwidth_kbps{server="elfhame",session="one",user="alice",location="lan"} 1000
plex_session_bandwidth_kbps{server="elfhame",session="two",user="bob",location="lan"} 2500
# HELP plex_play_seconds_total Play seconds
# TYPE plex_play_seconds_total counter
plex_play_seconds_total{title="Movie A",user="alice",session="one",stream_type="directplay",transcode_type="none",media_type="movie",location="lan",local="true"} 30
# EOF
"""
        output = sanitize_metrics(raw)
        self.assertIn("plex_server_info", output)
        self.assertIn(
            'plex_plays_active{local="true",location="lan",media_type="movie",stream_type="directplay",transcode_type="none"} 2',
            output,
        )
        self.assertIn('plex_session_bandwidth_kbps{location="lan"} 3500', output)
        self.assertIn("plex_sanitized_sessions_active 2", output)
        self.assertIn(
            'plex_sanitized_sessions_by_stream_type{stream_type="directplay"} 2',
            output,
        )
        self.assertIn(
            'plex_sanitized_sessions_by_stream_type{stream_type="copy"} 0', output
        )
        self.assertIn("plex_sanitized_session_bandwidth_kbps 3500", output)
        for unsafe in ("title=", "user=", "session=", "device=", "Movie A", "alice"):
            self.assertNotIn(unsafe, output)
        self.assertNotIn("plex_play_seconds_total", output)

    def test_missing_required_label_fails_closed(self):
        raw = 'plex_plays_active{stream_type="directplay"} 1\n'
        with self.assertRaisesRegex(RuntimeError, "missing required labels"):
            sanitize_metrics(raw)

    def test_openmetrics_eof_is_removed(self):
        output = sanitize_metrics("metric_without_labels 1\n# EOF\n")
        self.assertIn("metric_without_labels 1\n", output)
        self.assertNotIn("# EOF", output)
        self.assertIn("plex_sanitized_sessions_active 0", output)

    def test_library_duration_is_normalized_to_base_seconds(self):
        raw = """# HELP plex_library_duration_milliseconds Duration in ms
# TYPE plex_library_duration_milliseconds gauge
plex_library_duration_milliseconds{library="Movies"} 12500
"""
        output = sanitize_metrics(raw)
        self.assertNotIn("milliseconds", output)
        self.assertIn("# TYPE plex_library_duration_seconds gauge", output)
        self.assertIn('plex_library_duration_seconds{library="Movies"} 12.5', output)


if __name__ == "__main__":
    unittest.main()
