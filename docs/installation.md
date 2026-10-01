# plex-monitoring — Installation

## Requirements

Docker Compose, Plex token, upstream cplieger/plex-exporter, Prometheus and Grafana.

## Procedure

Copy .env.example to .env and set PLEX_URL. Create secrets/plex-token and secrets/metrics-token, then docker compose up -d --build. Adapt examples/prometheus-scrape.yml and import dashboards/plex-application.json.

The files under [examples](../examples) are reference configuration. Replace example addresses, token paths and bind addresses for your deployment.

Next, review [configuration](./configuration.md) and [dashboard usage](./usage.md).

## Compose lifecycle

From the repository root run `docker compose up -d --build` when Compose builds a local image, or `docker compose up -d` for prebuilt images. Inspect container output with `docker compose logs`. Keep credential files out of Git.
