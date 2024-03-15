FROM pgvector/pgvector:pg16

ENV POSTGRES_PASSWORD=pwd \
    POSTGRES_USER=user \
    POSTGRES_DB=postgres

COPY ./init.sql /docker-entrypoint-initdb.d/

EXPOSE 5432