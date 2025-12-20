#!/bin/bash

DB_SERVICE="db"
PS_SERVICE="prestashop"
DB_USER="root"
DB_PASSWD="admin"
DB_NAME="prestashop_db"

BACKUP_DIR="backups"
BACKUP_NAME="${1:-}"

if [ -z "$BACKUP_NAME" ]; then
    echo "use: ./restore.sh <backup_folder_name>"
    echo ""
    echo "available backups:"
    ls -1d "$BACKUP_DIR"/* 2>/dev/null | xargs -n1 basename || echo "(no backups found)"
    exit 1
fi

BACKUP_PATH="${BACKUP_DIR}/${BACKUP_NAME}"
DUMP_FILE="${BACKUP_PATH}/prestashop_dump.sql"

if [ ! -d "$BACKUP_PATH" ]; then
    echo "backup not found: $BACKUP_PATH"
    exit 1
fi

echo "restoring backup: $BACKUP_NAME "

# 1. database
if [ ! -f "$DUMP_FILE" ]; then
    echo "sql file not found: $DUMP_FILE"
    exit 1
fi

cat "$DUMP_FILE" | docker compose -f ../docker-compose.yml exec -T $DB_SERVICE mysql \
  -u"$DB_USER" \
  -p"$DB_PASSWD" \
  "$DB_NAME" 2>&1 | grep -v "using a password"

if [ $? -eq 0 ]; then
    echo "database restored"
else
    echo "error restoring database"
    exit 1
fi

# 2. images
IMG_PATH="${BACKUP_PATH}/img"

if [ -d "$IMG_PATH" ]; then
    docker compose -f ../docker-compose.yml cp "$IMG_PATH" "$PS_SERVICE:/var/www/html/"
    
    if [ $? -eq 0 ]; then
        echo "images restored"
    else
        echo "error restoring images"
    fi
else
    echo "imges folder not found"
fi

# 3. upload
UPLOAD_PATH="${BACKUP_PATH}/upload"
DOWNLOAD_PATH="${BACKUP_PATH}/download"

if [ -d "$UPLOAD_PATH" ]; then
    docker compose -f ../docker-compose.yml cp "$UPLOAD_PATH" "$PS_SERVICE:/var/www/html/"
    echo "upload restored"
fi

if [ -d "$DOWNLOAD_PATH" ]; then
    docker compose -f ../docker-compose.yml cp "$DOWNLOAD_PATH" "$PS_SERVICE:/var/www/html/"
    echo "download restored"
fi

# 4. cache
docker compose -f ../docker-compose.yml exec -T $PS_SERVICE \
  bash -c "rm -rf /var/www/html/var/cache/prod/* /var/www/html/var/cache/dev/* /var/www/html/var/logs/*" 2>/dev/null

echo ""
echo "restore completed"
echo "shop restored successfully"
