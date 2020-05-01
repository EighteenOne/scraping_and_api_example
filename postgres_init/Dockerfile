FROM postgres:12

COPY ./init_app_db.sh /docker-entrypoint-initdb.d/init_app_db.sh
RUN chmod a+x /docker-entrypoint-initdb.d/init_app_db.sh