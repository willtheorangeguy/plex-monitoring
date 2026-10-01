# Development guide

The implementation and dashboard definitions are in the repository root. Plex -> upstream exporter -> sanitizer that drops or aggregates session identity labels -> authenticated /metrics -> Prometheus -> Grafana.

## Local checks

The repository CI workflow runs `python -m unittest discover -s sanitizer/tests -v`. Run it from the repository root after changing the relevant source or dashboard JSON.

When editing dashboards, export the final JSON from Grafana and keep data source variables, job names and panel descriptions in sync with [configuration](configuration.md).

The privacy boundary is [sanitizer/src/plex_metrics_sanitizer.py](https://github.com/willtheorangeguy/plex-monitoring/blob/HEAD/sanitizer/src/plex_metrics_sanitizer.py). Review the kept metric families and labels before adding upstream metrics. The [Compose file](https://github.com/willtheorangeguy/plex-monitoring/blob/HEAD/compose.yml) leaves the upstream exporter on the internal network and publishes only the sanitizer. [Sanitizer tests](https://github.com/willtheorangeguy/plex-monitoring/tree/HEAD/sanitizer/tests) cover exposition changes and redaction behavior.
