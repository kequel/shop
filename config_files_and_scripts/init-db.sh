#!/bin/bash
set -e

DB_HOST="student-swarm01.maas"
DB_PORT="3306"
DB_USER="root"
DB_PASSWORD="admin"
DB_NAME="RSWW_123456_prestashop"  # ZMIEŃ NA SWÓJ PREFIX!

echo "Waiting for MySQL server..."
until mysql -h"$DB_HOST" -P"$DB_PORT" -u"$DB_USER" -p"$DB_PASSWORD" -e "SELECT 1" &>/dev/null; do
  echo "MySQL not ready yet..."
  sleep 2
done

echo "Creating database if not exists..."
mysql -h"$DB_HOST" -P"$DB_PORT" -u"$DB_USER" -p"$DB_PASSWORD" -e "CREATE DATABASE IF NOT EXISTS $DB_NAME;"

echo "Checking if database is empty..."
TABLE_COUNT=$(mysql -h"$DB_HOST" -P"$DB_PORT" -u"$DB_USER" -p"$DB_PASSWORD" -N -e "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='$DB_NAME';")

if [ "$TABLE_COUNT" -eq "0" ]; then
  echo "Database is empty. Importing dump..."
  mysql -h"$DB_HOST" -P"$DB_PORT" -u"$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" < /tmp/prestashop_dump.sql
  echo "Database initialized successfully!"
else
  echo "Database already contains $TABLE_COUNT tables. Skipping initialization."
fi