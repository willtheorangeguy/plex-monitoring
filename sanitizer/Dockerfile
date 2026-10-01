FROM python:3.13-alpine

WORKDIR /app
COPY src/plex_metrics_sanitizer.py /app/plex_metrics_sanitizer.py

EXPOSE 9594
ENTRYPOINT ["python3", "/app/plex_metrics_sanitizer.py"]
