# Troubleshooting

| Symptom | Check |
| --- | --- |
| Sanitizer /healthz returns 503 | inspect upstream reachability and exposition format. |
| /metrics returns 401 | check secrets/metrics-token and Prometheus credentials_file. |
| Session panels blank while library panels work | check upstream session polling and sanitizer health. |

## First checks

Check the selected Grafana data source and dashboard variables in [configuration](configuration.md). For Prometheus, inspect the target state and the exact job and instance labels before changing panel queries.
