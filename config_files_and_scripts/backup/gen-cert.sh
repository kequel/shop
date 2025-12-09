#!/bin/bash

CERT_DIR="../../docker/certs"
CONF_FILE="./openssl.conf"

KEY_FILE="$CERT_DIR/prestashop.key"
CRT_FILE="$CERT_DIR/prestashop.crt"

if [ ! -d "$CERT_DIR" ]; then
    mkdir -p "$CERT_DIR"
fi

if [ ! -f "$CONF_FILE" ]; then
    echo "no $CONF_FILE file"
    exit 1
fi

echo "generating SSL..."
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout "$KEY_FILE" \
    -out "$CRT_FILE" \
    -config "$CONF_FILE" \
    -extensions v3_req

if [ $? -eq 0 ]; then
    echo "cert generated in $CERT_DIR"
else
    echo "error in generating certs"
fi
