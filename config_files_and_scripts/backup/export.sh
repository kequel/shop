#!/bin/bash

DB_SERVICE="db"
DB_USER="root"
DB_PASSWD="admin"
DB_NAME="prestashop_db"

FILENAME="prestashop_dump.sql"

docker compose -f ../docker-compose.yml exec -T $DB_SERVICE mysqldump \
  -u"$DB_USER" \
  -p"$DB_PASSWD" \
  "$DB_NAME" \
  > "$FILENAME"

if [ $? -eq 0 ] && [ -s "$FILENAME" ]; then
    echo "succesfully exported"
else
    echo "could not export"
    exit 1
fi
