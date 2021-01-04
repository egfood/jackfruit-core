#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE USER $POSTGRES_DB_USER WITH password '$POSTGRES_DB_USER_PASSWORD';
    ALTER USER $POSTGRES_DB_USER WITH CREATEDB;
    ALTER USER $POSTGRES_DB_USER WITH CREATEROLE;
    CREATE DATABASE $POSTGRES_DB_NAME;
    GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB_NAME TO $POSTGRES_DB_USER;
EOSQL
psql --username "$POSTGRES_USER" -d "$POSTGRES_DB_NAME" -c "ALTER USER $POSTGRES_DB_USER WITH SUPERUSER"
psql --username "$POSTGRES_USER" -d "$POSTGRES_DB_NAME" -c "CREATE SCHEMA AUTHORIZATION $POSTGRES_DB_SCHEMA"

echo "# General settings" >> /var/lib/postgresql/data/postgresql.conf
echo "default_transaction_isolation = 'read committed'" >> /var/lib/postgresql/data/postgresql.conf
echo "timezone = 'UTC'" >> /var/lib/postgresql/data/postgresql.conf
echo "client_encoding = 'UTF8'" >> /var/lib/postgresql/data/postgresql.conf

echo "# Performance tuning by http://pgtune.leopard.in.ua" >> /var/lib/postgresql/data/postgresql.conf
echo "max_connections = $POSTGRES_CONFIG_MAX_CONNECTIONS" >> /var/lib/postgresql/data/postgresql.conf
echo "shared_buffers = $POSTGRES_CONFIG_SHARED_BUFFERS" >> /var/lib/postgresql/data/postgresql.conf
echo "effective_cache_size = $POSTGRES_CONFIG_EFFECTIVE_CACHE_SIZE" >> /var/lib/postgresql/data/postgresql.conf
echo "work_mem = $POSTGRES_CONFIG_WORK_MEM" >> /var/lib/postgresql/data/postgresql.conf
echo "maintenance_work_mem = $POSTGRES_CONFIG_MAINTENANCE_WORK_MEM" >> /var/lib/postgresql/data/postgresql.conf
echo "min_wal_size = $POSTGRES_CONFIG_MIN_WAL_SIZE" >> /var/lib/postgresql/data/postgresql.conf
echo "max_wal_size = $POSTGRES_CONFIG_MAX_WAL_SIZE" >> /var/lib/postgresql/data/postgresql.conf
echo "checkpoint_completion_target = $POSTGRES_CONFIG_CHECKPOINT_COMPLETION_TARGET" >> /var/lib/postgresql/data/postgresql.conf
echo "wal_buffers = $POSTGRES_CONFIG_WAL_BUFFERS" >> /var/lib/postgresql/data/postgresql.conf
echo "default_statistics_target = $POSTGRES_CONFIG_DEFAULT_STATISTICS_TARGET" >> /var/lib/postgresql/data/postgresql.conf
echo "random_page_cost = $POSTGRES_CONFIG_RANDOM_PAGE_COST" >> /var/lib/postgresql/data/postgresql.conf
