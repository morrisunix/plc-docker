#!/bin/sh
set -e

echo "[$(date)] Starting backup process..."

# Check required environment variables
if [ -z "$AWS_S3_BUCKET" ]; then
    echo "ERROR: AWS_S3_BUCKET is not set."
    exit 1
fi

# Variables
S3_PATH="s3://${AWS_S3_BUCKET}/${AWS_S3_PATH:-backups}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="/tmp/backup_${TIMESTAMP}.tar.gz"

echo "[$(date)] Creating tarball of /backup/influxdb and /backup/plc_layout.yml..."
if [ ! -d "/backup/influxdb" ]; then
    echo "ERROR: /backup/influxdb directory not found."
    exit 1
fi

if [ ! -f "/backup/plc_layout.yml" ]; then
    echo "ERROR: /backup/plc_layout.yml file not found."
    exit 1
fi

tar -czf ${BACKUP_FILE} -C /backup influxdb plc_layout.yml

echo "[$(date)] Uploading ${BACKUP_FILE} to ${S3_PATH}/backup_${TIMESTAMP}.tar.gz..."
aws s3 cp ${BACKUP_FILE} ${S3_PATH}/backup_${TIMESTAMP}.tar.gz

echo "[$(date)] Cleaning up..."
rm ${BACKUP_FILE}

echo "[$(date)] Backup completed successfully."
