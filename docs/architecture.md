# plex-monitoring — Architecture

Plex -> upstream exporter -> sanitizer that drops or aggregates session identity labels -> authenticated /metrics -> Prometheus -> Grafana.

## Components

- [compose.yml](../compose.yml): container deployment
- [dashboards/](../dashboards): Grafana dashboard definitions
- [examples/](../examples): deployment and scrape examples
- [sanitizer/](../sanitizer): Plex sanitization implementation

## Data interpretation

Only the sanitizer should be scraped or published. It strips session identity labels, emits bounded stream and transcode aggregates, and converts library duration from milliseconds to seconds. Exposing the raw exporter can reveal session identity.
