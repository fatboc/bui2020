FROM yiisoftware/yii2-php:7.4-apache
WORKDIR /app
EXPOSE 80
RUN docker-php-ext-install sockets
RUN docker-php-ext-install bcmath
COPY basic /app
RUN chmod -R 777 web/assets
RUN /etc/init.d/apache2 start
