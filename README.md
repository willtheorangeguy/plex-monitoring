# Plex metrics sanitizer and application dashboard

Portable monitoring bundle with example configuration. Replace example addresses and token paths for your installation; no live credentials are included.

## Requirements

The upstream cplieger/plex-exporter and the included sanitizer. The sanitizer removes session identity labels before Prometheus sees them.

## Dashboards

- `dashboards/plex-application.json`

Import the JSON in Grafana using **Dashboards > New > Import**. Select your data source from the dashboard variable(s) at the top. Update the Prometheus job variables to match your `scrape_configs` job names; use the Instance selector when present. The dashboard's JSON is also suitable for file provisioning after you have selected or provisioned data source UIDs.

Expected default job labels:

- `plex-application.json`: plex

## Monitoring code

See the code and example configuration in this folder, if present. Keep API keys and metrics bearer tokens in local secret files or another secret manager; never commit them. Scrape examples use documentation addresses and must be edited for your network.

## Before publishing

Test against the application and Grafana versions you intend to support. Add a license you choose and check attribution for upstream components. No release or Grafana catalog upload has been performed.

## Run the sanitizer

Copy `.env.example` to `.env`; set `PLEX_URL` to your Plex server. Create `secrets/plex-token` with the Plex token and `secrets/metrics-token` with an independent bearer token. Run `docker compose up -d --build`. Only the sanitizer is published; do not expose the raw upstream exporter because it includes session identity labels. Scrape the sanitizer as job `plex` with the metrics bearer token. Run `python -m unittest discover -s sanitizer/tests -v` before release.

A sample `scrape_configs` fragment is in `examples/prometheus-scrape.yml`; replace the example hosts and token paths.
