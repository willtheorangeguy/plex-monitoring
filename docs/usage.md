# plex-monitoring — Dashboard Usage

Import the JSON files using **Grafana → Dashboards → New → Import**. Set the data source and variables listed in [configuration](./configuration.md).

## Plex Application Overview

Source: [plex-application.json](../dashboards/plex-application.json). Refresh: `30s`.

<!-- Screenshot: after adding plex-application.png to .github/icons/plex-monitoring/, replace this comment with ![Plex Application Overview](https://raw.githubusercontent.com/willtheorangeguy/.github/main/icons/plex-monitoring/plex-application.png). -->

### Panels

| Panel | Type | What it shows |
|---|---|---|
| Service Health | stat | Prometheus scrape, Plex HTTP API, session polling, and the sanitizer must all be healthy. |
| Active Sessions | stat | Total active Plex playback sessions without viewer or media identity labels. |
| Direct Play | stat | Sessions whose video and audio are played directly by the client. |
| Direct Stream | stat | Direct-stream sessions. The upstream exporter calls this bounded playback decision 'copy'. |
| Transcodes | stat | Sessions currently requiring a video or audio transcode. |
| Session Bandwidth | stat | Aggregate bandwidth reported for all active sessions. |
| Libraries | stat | Distinct Plex libraries represented in the exporter inventory. |
| Media Storage | stat | Total logical media bytes reported across all Plex libraries. |
| Sessions by Playback Decision | timeseries | Active sessions grouped only by the bounded playback decision emitted by the sanitizer. |
| Sessions by Transcode Type | timeseries | Active sessions grouped by whether Plex is transcoding video, audio, both, or neither. |
| Active-session Bandwidth | timeseries | Aggregate bandwidth requested by active Plex sessions. |
| Plex Transmit Throughput | timeseries | Rate of bytes transmitted by Plex according to the server's cumulative counter. |
| Catalog by Media Type | bargauge | Exact catalog counts grouped by Plex content type. Episodes, movies, and tracks are distinct units and are not combined into a synthetic total. |
| Storage by Library Type | bargauge | Logical media bytes grouped by Plex library type. |
| Duration by Library Type | bargauge | Total playable duration grouped by Plex library type. |
| Items by Library | bargauge | Exact catalog count for each Plex library, using that library's native content unit. |
| Storage by Library | bargauge | Logical storage occupied by each Plex library. |
| Duration by Library | bargauge | Total playable duration in each Plex library. |
| Plex Metrics Health History | timeseries | Independent availability history for Prometheus scraping, the Plex API, session polling, and sanitization. |
| Exporter Failures | timeseries | Cumulative failures while fetching or sanitizing upstream metrics. The current value is real and is not converted into a synthetic rate. |
| Metrics Collection Duration | timeseries | Duration of the most recent exporter fetch and privacy-sanitization pass. |

<!-- Screenshot: add a focused panel or section image here after uploading it to .github/icons/plex-monitoring/. -->

### Reading the results

Only the sanitizer should be scraped or published. It strips session identity labels, emits bounded stream and transcode aggregates, and converts library duration from milliseconds to seconds. Exposing the raw exporter can reveal session identity.

### Query reference

These expressions are copied from the dashboard JSON. Grafana substitutes the dashboard variables at runtime.

#### Service Health

```promql
min(up{job="${job_plex}",instance="$instance"} or plex_http_reachable{job="${job_plex}",instance="$instance"} or plex_session_poll_reachable{job="${job_plex}",instance="$instance"} or plex_sanitizer_up{job="${job_plex}",instance="$instance"})
```

#### Active Sessions

```promql
plex_sanitized_sessions_active{job="${job_plex}",instance="$instance"}
```

#### Direct Play

```promql
plex_sanitized_sessions_by_stream_type{job="${job_plex}",instance="$instance",stream_type="directplay"}
```

#### Direct Stream

```promql
plex_sanitized_sessions_by_stream_type{job="${job_plex}",instance="$instance",stream_type="copy"}
```

#### Transcodes

```promql
plex_sanitized_sessions_by_stream_type{job="${job_plex}",instance="$instance",stream_type="transcode"}
```

#### Session Bandwidth

```promql
plex_sanitized_session_bandwidth_kbps{job="${job_plex}",instance="$instance"}
```

#### Libraries

```promql
count(count by (library_id) (plex_library_items{job="${job_plex}",instance="$instance"}))
```

#### Media Storage

```promql
sum(plex_library_storage_bytes{job="${job_plex}",instance="$instance"})
```

#### Sessions by Playback Decision

```promql
plex_sanitized_sessions_by_stream_type{job="${job_plex}",instance="$instance"}
```

#### Sessions by Transcode Type

```promql
plex_sanitized_sessions_by_transcode_type{job="${job_plex}",instance="$instance"}
```

#### Active-session Bandwidth

```promql
plex_sanitized_session_bandwidth_kbps{job="${job_plex}",instance="$instance"}
```

#### Plex Transmit Throughput

```promql
rate(plex_transmit_bytes_total{job="${job_plex}",instance="$instance"}[$__rate_interval])
```

#### Catalog by Media Type

```promql
sum by (content_type) (plex_library_items{job="${job_plex}",instance="$instance"})
```

#### Storage by Library Type

```promql
sum by (library_type) (plex_library_storage_bytes{job="${job_plex}",instance="$instance"})
```

#### Duration by Library Type

```promql
sum by (library_type) (plex_library_duration_seconds{job="${job_plex}",instance="$instance"})
```

#### Items by Library

```promql
sort_desc(plex_library_items{job="${job_plex}",instance="$instance"})
```

#### Storage by Library

```promql
sort_desc(plex_library_storage_bytes{job="${job_plex}",instance="$instance"})
```

#### Duration by Library

```promql
sort_desc(plex_library_duration_seconds{job="${job_plex}",instance="$instance"})
```

#### Plex Metrics Health History

```promql
up{job="${job_plex}",instance="$instance"}
plex_http_reachable{job="${job_plex}",instance="$instance"}
plex_session_poll_reachable{job="${job_plex}",instance="$instance"}
plex_sanitizer_up{job="${job_plex}",instance="$instance"}
```

#### Exporter Failures

```promql
plex_sanitizer_failures_total{job="${job_plex}",instance="$instance"}
plex_exporter_errors_total{job="${job_plex}",instance="$instance"}
```

#### Metrics Collection Duration

```promql
plex_sanitizer_fetch_duration_seconds{job="${job_plex}",instance="$instance"}
```
