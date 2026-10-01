# FAQ

## Common questions

???+ question "Why are dashboard panels empty?"

    Check that the scrape jobs or Loki labels listed on [Getting started](getting-started.md) are present. Then select the matching data source, job and instance values in Grafana.

??? question "Which dashboard file should I import?"

    Import [`dashboards/plex-application.json`](https://github.com/willtheorangeguy/plex-monitoring/blob/HEAD/dashboards/plex-application.json). The [Dashboard usage](usage.md) page describes its variables.

??? question "Which Prometheus jobs should I configure?"

    plex Use the repository scrape example when one is provided. See [Configuration](configuration.md).

## Troubleshooting

See [Troubleshooting](troubleshooting.md) for symptoms and checks based on this repository's integrations.

## Getting help

{{ support() }}
