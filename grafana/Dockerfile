# Stage 1: Generate provisioning file
FROM python:3.11-slim as generator
WORKDIR /app

# Build arguments for provisioning generation
ARG INFLUXDB_ADMIN_USER
ARG INFLUXDB_ADMIN_PASSWORD
ARG INFLUXDB_HOST

# Set environment variables for the script to use during the RUN command
ENV INFLUXDB_ADMIN_USER=$INFLUXDB_ADMIN_USER
ENV INFLUXDB_ADMIN_PASSWORD=$INFLUXDB_ADMIN_PASSWORD
ENV INFLUXDB_HOST=$INFLUXDB_HOST

RUN pip install pyyaml
COPY plc_layout.yml .
COPY grafana/generate_provisioning.py ./grafana/
RUN python grafana/generate_provisioning.py

# Stage 2: Final Grafana image
FROM grafana/grafana:latest

# Copy the generated InfluxDB datasource configuration file from stage 1
COPY --from=generator /app/grafana/influxdb.yaml ${GF_PATHS_PROVISIONING}/datasources/

# Copy the generated dashboards configuration file from stage 1
COPY grafana/dashboards.yml ${GF_PATHS_PROVISIONING}/dashboards/

# Expose the default Grafana HTTP port
EXPOSE 3000
