FROM mariadb

ENV MYSQL_RANDOM_ROOT_PASSWORD=yes
ENV MYSQL_USER=bui2020
ENV MYSQL_PASSWORD=BUI-zimowy-2020
ENV MYSQL_DATABASE=studia
COPY init.sql /docker-entrypoint-initdb.d/
EXPOSE 3306
