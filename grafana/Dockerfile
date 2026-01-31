# Stage 1: Generate provisioning file
FROM python:3.11-slim as generator
WORKDIR /app
RUN pip install pyyaml
COPY plc_layout.yml .
COPY grafana/generate_provisioning.py ./grafana/
RUN python grafana/generate_provisioning.py

# Stage 2: Final Grafana image
FROM grafana/grafana:latest

# Create the directory for datasources provisioning within the image
# RUN mkdir -p ${GF_PATHS_PROVISIONING}/datasources

# Copy the generated InfluxDB datasource configuration file from stage 1
COPY --from=generator /app/grafana/influxdb.yaml ${GF_PATHS_PROVISIONING}/datasources/

# Create the directory for dashboards provisioning within the image
# RUN mkdir -p ${GF_PATHS_PROVISIONING}/dashboards

# Copy the generated dashboards configuration file from stage 1
COPY grafana/dashboards.yml ${GF_PATHS_PROVISIONING}/dashboards/

# Expose the default Grafana HTTP port
EXPOSE 3000

# The default command for Grafana (grafana-server) is already defined in the base image
# and will pick up the provisioning files automatically.
# CMD ["grafana-server", "--homepath", "/usr/share/grafana", "--config", "/etc/grafana/grafana.ini"]

