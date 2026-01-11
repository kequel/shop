FROM prestashop/prestashop:1.7-apache

RUN apt-get update && apt-get install -y \
    vim \
    curl \
    ssl-cert \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

RUN a2enmod ssl rewrite headers

RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/ssl/private/apache-selfsigned.key \
    -out /etc/ssl/certs/apache-selfsigned.crt \
    -subj "/C=PL/ST=Pomorskie/L=Gdansk/O=PJATK/OU=BE/CN=localhost"

RUN sed -i 's|/etc/ssl/certs/ssl-cert-snakeoil.pem|/etc/ssl/certs/apache-selfsigned.crt|g' /etc/apache2/sites-available/default-ssl.conf && \
    sed -i 's|/etc/ssl/private/ssl-cert-snakeoil.key|/etc/ssl/private/apache-selfsigned.key|g' /etc/apache2/sites-available/default-ssl.conf

RUN a2ensite default-ssl

COPY docker/init-db.sh /init-db.sh
COPY docker/prestashop_dump.sql /tmp/prestashop_dump.sql
COPY store_source_code /var/www/html

RUN chmod +x /init-db.sh && \
    chown -R www-data:www-data /var/www/html

EXPOSE 80 443
