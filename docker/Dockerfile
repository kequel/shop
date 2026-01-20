FROM prestashop/prestashop:1.7-apache

RUN apt-get update && apt-get install -y \
    default-mysql-client \
    ssl-cert \
    libmemcached-dev \
    zlib1g-dev \
    && printf "\n" | pecl install memcached \
    && docker-php-ext-enable memcached \
    && rm -rf /var/lib/apt/lists/*

RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/ssl/private/ssl-cert-snakeoil.key \
    -out /etc/ssl/certs/ssl-cert-snakeoil.pem \
    -subj "/C=PL/ST=Pomorskie/L=Gdansk/O=PJATK/OU=BE/CN=localhost"

RUN a2enmod ssl rewrite headers && a2ensite default-ssl

RUN rm -rf /var/www/html/*
COPY --chown=33:33 ./store_source_code /var/www/html

COPY docker/init-db.sh /init-db.sh
COPY docker/prestashop_dump.sql /tmp/prestashop_dump.sql

RUN rm -rf /var/www/html/install /var/www/html/install-dev && \
    chmod +x /init-db.sh

ENTRYPOINT ["/init-db.sh"]
EXPOSE 80 443
