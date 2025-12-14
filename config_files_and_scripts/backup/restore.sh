#!/bin/bash

DB_SERVICE="db"
PS_SERVICE="prestashop"
DB_USER="root"
DB_PASSWD="admin"
DB_NAME="prestashop_db"

BACKUP_DIR="backups"
BACKUP_NAME="${1:-}"

if [ -z "$BACKUP_NAME" ]; then
    echo "use: ./restore.sh <nazwa_backupu>"
    echo ""
    echo available backups:"
    ls -1d "$BACKUP_DIR"/* 2>/dev/null | xargs -n1 basename || echo "(no backups found)"
    exit 1
fi

BACKUP_PATH="${BACKUP_DIR}/${BACKUP_NAME}"
DUMP_FILE="${BACKUP_PATH}/prestashop_dump.sql"

if [ ! -d "$BACKUP_PATH" ]; then
    echo "backup not found: $BACKUP_PATH"
    exit 1
fi

# 1. database
if [ ! -f "$DUMP_FILE" ]; then
    echo "sql file not found: $DUMP_FILE"
    exit 1
fi

cat "$DUMP_FILE" | docker compose -f ../docker-compose.yml exec -T $DB_SERVICE mysql \
  -u"$DB_USER" \
  -p"$DB_PASSWD" \
  "$DB_NAME" 2>&1 | grep -v "Using a password"

if [ $? -eq 0 ]; then
    echo "data base restored"
else
    echo "error in import data base"
    exit 1
fi

# 2. images
IMAGES_BACKUP="${BACKUP_PATH}/img.tar.gz"

if [ -f "$IMAGES_BACKUP" ]; then
    docker compose -f ../docker-compose.yml cp "$IMAGES_BACKUP" "$PS_SERVICE:/tmp/img_backup.tar.gz"
    
    docker compose -f ../docker-compose.yml exec -T $PS_SERVICE \
      bash -c "cd /var/www/html && tar -xzf /tmp/img_backup.tar.gz && rm /tmp/img_backup.tar.gz"
    
    if [ $? -eq 0 ]; then
        echo "images restored"
    else
        echo "error in restoring images"
    fi
else
    echo "no img.tar.gz found"
fi

# 3. upload/download
UPLOAD_BACKUP="${BACKUP_PATH}/upload.tar.gz"

if [ -f "$UPLOAD_BACKUP" ]; then
    docker compose -f ../docker-compose.yml cp "$UPLOAD_BACKUP" "$PS_SERVICE:/tmp/upload_backup.tar.gz"
    
    docker compose -f ../docker-compose.yml exec -T $PS_SERVICE \
      bash -c "cd /var/www/html && tar -xzf /tmp/upload_backup.tar.gz && rm /tmp/upload_backup.tar.gz"
    
    if [ $? -eq 0 ]; then
        echo "upload/download restored"
    else
        echo "warning: error restoring upload/download"
    fi
else
    echo "no upload/download found"
fi

# 4. Czyszczenie cache
echo "clearing cache"
docker compose -f ../docker-compose.yml exec -T $PS_SERVICE \
  bash -c "rm -rf /var/www/html/var/cache/prod/* /var/www/html/var/cache/dev/* /var/www/html/var/logs/*" 2>/dev/null

echo "restored successfully"