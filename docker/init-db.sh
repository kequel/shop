#!/bin/bash
set -e

DB_HOST="student-swarm01.maas"
DB_PORT="3306"
DB_USER="root"
DB_PASSWORD="student"
DB_NAME="BE_196615"

echo "Czekam na serwer MySQL..."
until mysql -h"$DB_HOST" -P"$DB_PORT" -u"$DB_USER" -p"$DB_PASSWORD" -e "SELECT 1" &>/dev/null; do
  echo "MySQL nie jest gotowy..."
  sleep 2
done

HAS_PRODUCTS=$(mysql -h"$DB_HOST" -P"$DB_PORT" -u"$DB_USER" -p"$DB_PASSWORD" -N -e "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='$DB_NAME' AND table_name='ps_product';")

if [ "$HAS_PRODUCTS" -eq "0" ]; then
  echo "Baza danych nie zawiera produktów. Rozpoczynam import dumpa..."
  if [ -f "/tmp/prestashop_dump.sql" ]; then
    mysql -h"$DB_HOST" -P"$DB_PORT" -u"$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" < /tmp/prestashop_dump.sql
    echo "Inicjalizacja zakończona sukcesem!"
  else
    echo "BŁĄD: Nie znaleziono pliku /tmp/prestashop_dump.sql w kontenerze!"
    exit 1
  fi
else
  echo "Produkty już istnieją w bazie $DB_NAME. Pomijam import."
fi
