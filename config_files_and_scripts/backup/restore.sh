#!/bin/bash

DB_SERVICE="db"
PS_SERVICE="prestashop"
DB_USER="root"
DB_PASSWD="admin"
DB_NAME="prestashop_db"

DUMP_FILE="prestashop_dump.sql"

if [ ! -f "$DUMP_FILE" ]; then
    echo "file not found"
    echo "did you make export.sh"
    exit 1
fi

cat "$DUMP_FILE" | docker compose -f ../docker-compose.yml exec -T $DB_SERVICE mysql -u"$DB_USER" -p"$DB_PASSWD" "$DB_NAME"

if [ $? -eq 0 ]; then
    echo "success, data base restored"
else
    echo "error in import data base"
    exit 1
fi

echo "clearing cache"
docker compose -f ../docker-compose.yml exec -T $PS_SERVICE bash -c "rm -rf /var/www/html/var/cache/prod/* /var/www/html/var/cache/dev/*" &>/dev/null

echo "restored successfully"
