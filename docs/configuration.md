# Configuration

## Precedence

This repository combines dashboard defaults with settings for external services. It defines no shared command-line, environment variable and configuration-file override order; each external service resolves its own settings.

## Integration settings

The upstream exporter is private inside Compose. The sanitizer publishes port 9594 on BIND_IP, which defaults to 127.0.0.1, and requires a bearer token at /metrics. The Python sanitizer also supports UPSTREAM_URL and UPSTREAM_TIMEOUT_SECONDS.

## Dashboard variables

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `plex-application.json / prometheus_ds` | datasource | `prometheus` | Grafana data source selected by the dashboard. |
| `plex-application.json / job_plex` | textbox | `plex` | Dashboard variable whose value selects a scrape job, instance or endpoint. |
| `plex-application.json / instance` | query | `label_values(up{job="${job_plex}"}, instance)` | Queries the data source for available values. |

## Prometheus jobs

The supplied [scrape example](https://github.com/willtheorangeguy/plex-monitoring/blob/HEAD/examples/prometheus-scrape.yml) defines `plex`. Copy its entries into your own scrape_configs and replace documentation hostnames. Job names can change if the dashboard variables change with them.

## Environment example

Start from [.env.example](https://github.com/willtheorangeguy/plex-monitoring/blob/HEAD/.env.example). Keep the resulting .env and all secret files outside version control.

## Examples

The complete scrape job examples are in [`examples/prometheus-scrape.yml`](https://github.com/willtheorangeguy/plex-monitoring/blob/HEAD/examples/prometheus-scrape.yml). Copy the relevant job into your Prometheus configuration and replace the example targets.
