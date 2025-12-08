# Backup and Configuration Scripts

This directory contains scripts and configuration files for managing the PrestaShop database and generating SSL certificates within the Docker environment.

## Prerequisites

All scripts **must** be executed from within this directory (`backup/`). They use the parent directory's configuration file (`../docker-compose.yml`).

## Scripts Summary

### 1. Database Backup (`./export.sh`)
Creates a database dump, saving it as `prestashop_dump.sql` in this folder. It connects to the `db` service.

### 2. Database Restore (`./restore.sh`)
Loads data from `prestashop_dump.sql` into the database and clears the PrestaShop cache in the `prestashop` container.

### 3. SSL Generation (`./gen-cert.sh`)
Generates self-signed SSL keys and certificates (`prestashop.key` and `prestashop.crt`) using the `openssl.conf` file. The output files are saved to `../../docker/certs`.

## Setup & Usage Flow

1.  **Permissions:** Ensure all scripts are executable:
    ```bash
    chmod +x export.sh restore.sh gen-cert.sh
    ```
2.  **Start Containers** (if not running):
    ```bash
    docker compose -f ../docker-compose.yml up -d
    ```
3.  **Generate SSL Keys** (Required for HTTPS setup):
    ```bash
    ./gen-cert.sh
    ```
4.  **Run Backup:**
    ```bash
    ./export.sh
    ```
