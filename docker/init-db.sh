#!/bin/bash
set -e

# 1. CZEKANIE NA BAZĘ
until mysql -h"$DB_SERVER" -u"$DB_USER" -p"$DB_PASSWORD" -e "SELECT 1" &>/dev/null; do
  sleep 3
done

# 2. BD IMPORT
mysql -h"$DB_SERVER" -u"$DB_USER" -p"$DB_PASSWORD" -e "CREATE DATABASE IF NOT EXISTS $DB_NAME;"
HAS_TABLES=$(mysql -h"$DB_SERVER" -u"$DB_USER" -p"$DB_PASSWORD" -N -e "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='$DB_NAME';")

if [ "$HAS_TABLES" -eq "0" ]; then
  if [ -f "/tmp/prestashop_dump.sql" ]; then
    mysql -h"$DB_SERVER" -u"$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" < /tmp/prestashop_dump.sql
  fi
fi

# 3. LINK, SSL
TARGET_DOMAIN="10.40.71.115"
OLD_URL="localhost:19662"

mysql -h"$DB_SERVER" -u"$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" -e "UPDATE ps_shop_url SET domain='$TARGET_DOMAIN', domain_ssl='$TARGET_DOMAIN', physical_uri='/' WHERE id_shop_url=1;"

mysql -h"$DB_SERVER" -u"$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" -e "UPDATE ps_configuration SET value = REPLACE(value, '$OLD_URL', '$TARGET_DOMAIN') WHERE value LIKE '%$OLD_URL%';"
mysql -h"$DB_SERVER" -u"$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" -e "UPDATE ps_cms_lang SET content = REPLACE(content, '$OLD_URL', '$TARGET_DOMAIN') WHERE content LIKE '%$OLD_URL%';"
mysql -h"$DB_SERVER" -u"$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" -e "UPDATE ps_product_lang SET description = REPLACE(description, '$OLD_URL', '$TARGET_DOMAIN') WHERE description LIKE '%$OLD_URL%';"

mysql -h"$DB_SERVER" -u"$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" -e "UPDATE ps_configuration SET value='1' WHERE name='PS_SSL_ENABLED';"
mysql -h"$DB_SERVER" -u"$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" -e "UPDATE ps_configuration SET value='1' WHERE name='PS_SSL_ENABLED_EVERYWHERE';"
mysql -h"$DB_SERVER" -u"$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" -e "UPDATE ps_configuration SET value='1' WHERE name='PS_REWRITING_SETTINGS';"

mysql -h"$DB_SERVER" -u"$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" -e "UPDATE ps_configuration SET value='1' WHERE name='PS_SMARTY_CACHE';"
mysql -h"$DB_SERVER" -u"$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" -e "UPDATE ps_configuration SET value='0' WHERE name='PS_SMARTY_FORCE_COMPILE';"
mysql -h"$DB_SERVER" -u"$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" -e "UPDATE ps_configuration SET value='V2' WHERE name='PS_SMARTY_CACHING_TYPE';"

# 4. KONFIGURACJA APACHE
a2enmod rewrite
sed -i '/<Directory \/var\/www\/>/,/<\/Directory>/ s/AllowOverride None/AllowOverride All/' /etc/apache2/apache2.conf

sed -i '/DocumentRoot \/var\/www\/html/a \        SetEnvIf X-Forwarded-Proto https HTTPS=on' /etc/apache2/sites-enabled/000-default.conf
if [ -f /etc/apache2/sites-enabled/default-ssl.conf ]; then
    sed -i '/DocumentRoot \/var\/www\/html/a \        SetEnvIf X-Forwarded-Proto https HTTPS=on' /etc/apache2/sites-enabled/default-ssl.conf
fi

# 5. PARAMETERS.PHP
PARAM_FILE="/var/www/html/app/config/parameters.php"
mkdir -p /var/www/html/app/config

cat <<EOF > $PARAM_FILE
<?php
return [
    'parameters' => [
        'database_host' => '$DB_SERVER',
        'database_port' => '',
        'database_name' => '$DB_NAME',
        'database_user' => '$DB_USER',
        'database_password' => '$DB_PASSWORD',
        'database_prefix' => 'ps_',
        'database_engine' => 'InnoDB',
        'secret' => 'a8b7c6d5e4f3g2h1i0j9k8l7m6n5o4p3',
        'ps_caching' => 'CacheMemcache',
        'ps_cache_enable' => false,
        'ps_creation_date' => '2026-01-19',
        'locale' => 'pl-PL',
        'cookie_key' => 'a8b7c6d5e4f3g2h1i0j9k8l7m6n5o4p3',
        'cookie_iv' => '12345678',
    ],
];
EOF
chown www-data:www-data $PARAM_FILE

# 6. GENEROWANIE .HTACCESS
php -d display_errors=Off -r "require_once('/var/www/html/config/config.inc.php'); Tools::generateHtaccess();"

# 7. PORZĄDKI
rm -rf /var/www/html/install /var/www/html/install-dev
rm -rf /var/www/html/var/cache/*

chown -R www-data:www-data /var/www/html/var/cache
[ -f /var/www/html/.htaccess ] && chown www-data:www-data /var/www/html/.htaccess

exec apache2-foreground
