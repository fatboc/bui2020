FROM yiisoftware/yii2-php:7.4-apache
WORKDIR /app
COPY basic /app
EXPOSE 80
RUN chmod -R 777 web/assets
RUN /etc/init.d/apache2 start
