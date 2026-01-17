#!/bin/bash
set -e

echo "Czekam na serwer MySQL ($DB_SERVER)..."
until mysql -h"$DB_SERVER" -u"$DB_USER" -p"$DB_PASSWORD" -e "SELECT 1" &>/dev/null; do
  sleep 3
done

mysql -h"$DB_SERVER" -u"$DB_USER" -p"$DB_PASSWORD" -e "CREATE DATABASE IF NOT EXISTS $DB_NAME;"

HAS_TABLES=$(mysql -h"$DB_SERVER" -u"$DB_USER" -p"$DB_PASSWORD" -N -e "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='$DB_NAME';")

if [ "$HAS_TABLES" -eq "0" ]; then
  if [ -f "/tmp/prestashop_dump.sql" ]; then
    mysql -h"$DB_SERVER" -u"$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" < /tmp/prestashop_dump.sql
  fi
fi

# TARGET_DOMAIN="10.40.71.115:19665"
TARGET_DOMAIN="127.0.0.1:19665"

mysql -h"$DB_SERVER" -u"$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" -e "UPDATE ps_shop_url SET domain='$TARGET_DOMAIN', domain_ssl='$TARGET_DOMAIN' WHERE id_shop_url=1;"
mysql -h"$DB_SERVER" -u"$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" -e "UPDATE ps_configuration SET value='1' WHERE name='PS_SSL_ENABLED';"
mysql -h"$DB_SERVER" -u"$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" -e "UPDATE ps_configuration SET value='1' WHERE name='PS_SSL_ENABLED_EVERYWHERE';"

rm -rf /var/www/html/var/cache/*

PARAM_FILE="/var/www/html/app/config/parameters.php"
if [ -f "$PARAM_FILE" ]; then
  sed -i "s/'database_host' => .*/'database_host' => '$DB_SERVER',/" $PARAM_FILE
  sed -i "s/'database_name' => .*/'database_name' => '$DB_NAME',/" $PARAM_FILE
  sed -i "s/'database_user' => .*/'database_user' => '$DB_USER',/" $PARAM_FILE
  sed -i "s/'database_password' => .*/'database_password' => '$DB_PASSWORD',/" $PARAM_FILE
fi

exec /tmp/docker_run.sh
