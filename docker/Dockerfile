# PrestaShop 1.7 with Apache
FROM prestashop/prestashop:1.7-apache

LABEL maintainer="Team BE_196615"
LABEL description="PrestaShop - BE Project"

# additional tools
RUN apt-get update && apt-get install -y \
    vim \
    curl \
    && rm -rf /var/lib/apt/lists/*

# SSL certificates
COPY certs/prestashop.crt /etc/ssl/certs/prestashop.crt
COPY certs/prestashop.key /etc/ssl/private/prestashop.key

# permissions for certificates
RUN chmod 600 /etc/ssl/private/prestashop.key

# enable required Apache modules
RUN a2enmod ssl rewrite headers \
    && a2ensite default-ssl

# ports
EXPOSE 80 443

# health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost/ || exit 1

# start Apache
CMD ["apache2-foreground"]
