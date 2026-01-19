FROM prestashop/prestashop:1.7-apache

RUN apt-get update && apt-get install -y \
    default-mysql-client \
    ssl-cert \
    unzip \
    git \
    && curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer \
    && rm -rf /var/lib/apt/lists/*

RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/ssl/private/ssl-cert-snakeoil.key \
    -out /etc/ssl/certs/ssl-cert-snakeoil.pem \
    -subj "/C=PL/ST=Pomorskie/L=Gdansk/O=PJATK/OU=BE/CN=localhost"

RUN a2enmod ssl rewrite headers && \
    a2ensite default-ssl

COPY docker/init-db.sh /init-db.sh
COPY docker/prestashop_dump.sql /tmp/prestashop_dump.sql
COPY store_source_code /var/www/html

WORKDIR /var/www/html
RUN composer install --no-dev --optimize-autoloader

RUN chmod +x /init-db.sh && \
    chown -R www-data:www-data /var/www/html

ENTRYPOINT ["/init-db.sh"]
EXPOSE 80 443
