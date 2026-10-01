# plex-monitoring — Quickstart

## Prerequisites

Docker Compose, Plex token, upstream cplieger/plex-exporter, Prometheus and Grafana.

## Set up

Copy .env.example to .env and set PLEX_URL. Create secrets/plex-token and secrets/metrics-token, then docker compose up -d --build. Adapt examples/prometheus-scrape.yml and import dashboards/plex-application.json.

The example Prometheus scrape job names are `plex`.

## Confirm data

In Prometheus, check `up{job="plex"}` and inspect a panel query in Grafana.
For missing data, see [troubleshooting](./troubleshooting.md).
