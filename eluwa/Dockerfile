FROM yiisoftware/yii2-php:7.4-apache
WORKDIR /app
COPY basic /app
EXPOSE 80
RUN docker-php-ext-install sockets
RUN comopser self-update
RUN composer require jonahgeorge/jaeger-client-php
RUN chmod -R 777 web/assets
RUN /etc/init.d/apache2 start
