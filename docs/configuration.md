# plex-monitoring — Configuration

The upstream exporter is private inside Compose. The sanitizer publishes port 9594 on BIND_IP, which defaults to 127.0.0.1, and requires a bearer token at /metrics. The Python sanitizer also supports UPSTREAM_URL and UPSTREAM_TIMEOUT_SECONDS.

## Dashboard variables

| Dashboard | Variable | Type | Default or query |
|---|---|---|---|
| `plex-application.json` | `prometheus_ds` | datasource | `prometheus` |
| `plex-application.json` | `job_plex` | textbox | `plex` |
| `plex-application.json` | `instance` | query | `label_values(up{job="${job_plex}"}, instance)` |

## Prometheus jobs

The supplied [scrape example](../examples/prometheus-scrape.yml) defines `plex`. Copy its entries into your own scrape_configs and replace documentation hostnames. Job names can change if the dashboard variables change with them.

## Environment example

Start from [.env.example](../.env.example). Keep the resulting .env and all secret files outside version control.
