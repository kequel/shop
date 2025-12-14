#!/bin/bash

DB_SERVICE="db"
PS_SERVICE="prestashop"
DB_USER="root"
DB_PASSWD="admin"
DB_NAME="prestashop_db"

BACKUP_DIR="backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_NAME="prestashop_backup_${TIMESTAMP}"
BACKUP_PATH="${BACKUP_DIR}/${BACKUP_NAME}"

mkdir -p "$BACKUP_DIR"
echo "backup timestamp: $TIMESTAMP"

# 1. database
DUMP_FILE="${BACKUP_PATH}/prestashop_dump.sql"
mkdir -p "$BACKUP_PATH"

docker compose -f ../docker-compose.yml exec -T $DB_SERVICE mysqldump \
  -u"$DB_USER" \
  -p"$DB_PASSWD" \
  "$DB_NAME" \
  > "$DUMP_FILE"

if [ $? -eq 0 ] && [ -s "$DUMP_FILE" ]; then
    DUMP_SIZE=$(du -h "$DUMP_FILE" | cut -f1)
else
    echo "data backup error"
    rm -rf "$BACKUP_PATH"
    exit 1
fi

# 2. img
IMAGES_BACKUP="${BACKUP_PATH}/img.tar.gz"

docker compose -f ../docker-compose.yml exec -T $PS_SERVICE \
  tar -czf /tmp/img_backup.tar.gz \
  -C /var/www/html img/ 2>/dev/null

if [ $? -eq 0 ]; then
    docker compose -f ../docker-compose.yml cp $PS_SERVICE:/tmp/img_backup.tar.gz "$IMAGES_BACKUP"
    docker compose -f ../docker-compose.yml exec -T $PS_SERVICE rm /tmp/img_backup.tar.gz
    
    IMG_SIZE=$(du -h "$IMAGES_BACKUP" | cut -f1)
else
    echo "could not backup images"
    IMAGES_BACKUP=""
fi

# 3. upload and download
UPLOAD_BACKUP="${BACKUP_PATH}/upload.tar.gz"

docker compose -f ../docker-compose.yml exec -T $PS_SERVICE \
  tar -czf /tmp/upload_backup.tar.gz \
  -C /var/www/html upload/ download/ 2>/dev/null

if [ $? -eq 0 ]; then
    docker compose -f ../docker-compose.yml cp $PS_SERVICE:/tmp/upload_backup.tar.gz "$UPLOAD_BACKUP"
    docker compose -f ../docker-compose.yml exec -T $PS_SERVICE rm /tmp/upload_backup.tar.gz
    
    UPLOAD_SIZE=$(du -h "$UPLOAD_BACKUP" | cut -f1)
else
    echo "upload/download not found"
fi

echo "backup ended"
