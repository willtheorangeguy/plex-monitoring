# Plex Monitoring

A privacy preserving relay for cplieger/plex-exporter, with a Grafana dashboard for playback, library inventory and health.

## Key features

- Session counts grouped without viewer identities.
- Library inventory and storage panels.
- Sanitizer health and upstream reachability metrics.
- Bearer protected metrics endpoint.

## Quick start

Open Grafana and import `dashboards/plex-application.json` through **Dashboards → New → Import**. Select the configured data source and match the dashboard variables to your labels. See [Getting started](getting-started.md) for prerequisites and setup.

## Where to next

<div class="wt-grid" markdown>

[:material-rocket-launch: **Getting started**<br>Set up the required integrations](getting-started.md){ .wt-card }

[:material-download: **Installation**<br>Install and connect the required services](installation.md){ .wt-card }

[:material-tune: **Configuration**<br>Review scrape examples and dashboard variables](configuration.md){ .wt-card }

[:material-sitemap: **Architecture**<br>Follow metrics from source to dashboard](architecture.md){ .wt-card }

[:material-view-dashboard: **Dashboard usage**<br>Import and use the dashboard](usage.md){ .wt-card }

</div>

## Support

{{ support() }}
