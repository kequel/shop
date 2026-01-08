FROM prestashop/prestashop:1.7-apache

# Instalacja narzędzi i certyfikatów
RUN apt-get update && apt-get install -y \
    vim \
    curl \
    ssl-cert \
    && rm -rf /var/lib/apt/lists/*

# Aktywacja modułów Apache
RUN a2enmod ssl rewrite headers

# Skrypt startowy, który upewni się, że SSL działa
RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/ssl/private/apache-selfsigned.key \
    -out /etc/ssl/certs/apache-selfsigned.crt \
    -subj "/C=PL/ST=Pomorskie/L=Gdansk/O=PJATK/OU=BE/CN=localhost"

# Zmiana domyślnej konfiguracji SSL
RUN sed -i 's|/etc/ssl/certs/ssl-cert-snakeoil.pem|/etc/ssl/certs/apache-selfsigned.crt|g' /etc/apache2/sites-available/default-ssl.conf && \
    sed -i 's|/etc/ssl/private/ssl-cert-snakeoil.key|/etc/ssl/private/apache-selfsigned.key|g' /etc/apache2/sites-available/default-ssl.conf

RUN a2ensite default-ssl

EXPOSE 80 443
