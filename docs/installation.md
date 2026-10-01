# Installation

## Requirements

Docker Compose, Plex token, upstream cplieger/plex-exporter, Prometheus and Grafana.

## Procedure

Copy .env.example to .env and set PLEX_URL. Create secrets/plex-token and secrets/metrics-token, then docker compose up -d --build. Adapt examples/prometheus-scrape.yml and import dashboards/plex-application.json.

The files under [examples](https://github.com/willtheorangeguy/plex-monitoring/tree/HEAD/examples) are reference configuration. Replace example addresses, token paths and bind addresses for your deployment.

Next, review [configuration](configuration.md) and [dashboard usage](usage.md).

## Compose lifecycle

From the repository root run `docker compose up -d --build` when Compose builds a local image, or `docker compose up -d` for prebuilt images. Inspect container output with `docker compose logs`. Keep credential files out of Git.

## Verify the installation

Check that the configured scrape target is healthy in Prometheus, then import the dashboard in Grafana and confirm its panels return data. Use the target and label names documented in [Getting started](getting-started.md).

## Upgrading

Update the dashboard JSON from this repository when you adopt a newer version. Update any exporter or monitored service using that project's upgrade instructions.

## Uninstalling

Remove the dashboard from Grafana and remove only the scrape or deployment entries you added for this project. Keep shared monitoring services that other dashboards use.
