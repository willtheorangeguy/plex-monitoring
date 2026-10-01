<h1 align="center">plex-monitoring</h1>
<h4 align="center">A privacy preserving relay for cplieger/plex-exporter, with a Grafana dashboard for playback, library inventory and health.</h4>

<div align="center">
  <img alt="GitHub Issues" src="https://img.shields.io/github/issues/willtheorangeguy/plex-monitoring">
  <img alt="GitHub Pull Requests" src="https://img.shields.io/github/issues-pr/willtheorangeguy/plex-monitoring">
  <img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue">
  <img alt="gitleaks workflow" src="https://github.com/willtheorangeguy/plex-monitoring/actions/workflows/gitleaks.yml/badge.svg">
  <img alt="testing workflow" src="https://github.com/willtheorangeguy/plex-monitoring/actions/workflows/testing.yml/badge.svg">
</div>

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#documentation">Documentation</a> •
  <a href="#support">Support</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#license">License</a>
</p>

<!-- Screenshot: after adding plex-monitoring/overview.png to .github/icons/, replace this comment with ![Dashboard overview](https://raw.githubusercontent.com/willtheorangeguy/.github/main/icons/plex-monitoring/overview.png). -->

A privacy preserving relay for cplieger/plex-exporter, with a Grafana dashboard for playback, library inventory and health.

## Key Features

- Session counts grouped without viewer identities.
- Library inventory and storage panels.
- Sanitizer health and upstream reachability metrics.
- Bearer protected metrics endpoint.

## Installation

Docker Compose, Plex token, upstream cplieger/plex-exporter, Prometheus and Grafana. Copy .env.example to .env and set PLEX_URL. Create secrets/plex-token and secrets/metrics-token, then docker compose up -d --build. Adapt examples/prometheus-scrape.yml and import dashboards/plex-application.json. See [installation](docs/installation.md) for more detail.

## Usage

Import [plex-application.json](dashboards/plex-application.json) in Grafana using **Dashboards → New → Import**. Choose the data source and match the dashboard variables to your monitoring labels. See [dashboard usage](docs/usage.md).

## Documentation

Full documentation lives in [docs/](docs/README.md): [Quickstart](docs/quickstart.md) · [Configuration](docs/configuration.md) · [Architecture](docs/architecture.md) · [Dashboard usage](docs/usage.md) · [Troubleshooting](docs/troubleshooting.md).

## Support

Open a [GitHub Discussion](https://github.com/willtheorangeguy/plex-monitoring/discussions/new) or file an [issue](https://github.com/willtheorangeguy/plex-monitoring/issues/new/choose).

## Contributing

Contributions welcome. See the org-wide [Contributing Guide](https://github.com/willtheorangeguy/.github/blob/main/CONTRIBUTING.md) and [Code of Conduct](https://github.com/willtheorangeguy/.github/blob/main/CODE_OF_CONDUCT.md).

## License

MIT — see [LICENSE.md](LICENSE.md).
