FROM python:3.12-slim
WORKDIR /usr/src/app/
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV OTEL_SERVICE_NAME=your-service-name
ENV OTEL_TRACES_EXPORTER=console,otlp
ENV OTEL_METRICS_EXPORTER=console
ENV OTEL_EXPORTER_OTLP_TRACES_ENDPOINT=0.0.0.0:4317
ENV DJANGO_SETTINGS_MODULE=oidc_app.settings
COPY src/ .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir opentelemetry-distro opentelemetry-exporter-otlp \
    && opentelemetry-bootstrap --action install
COPY ./entrypoint.sh .
RUN chmod +x ./entrypoint.sh
EXPOSE 8080
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
CMD ["opentelemetry-instrument", "python", "manage.py", "runserver", "0.0.0.0:8080"]