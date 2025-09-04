#!/bin/sh
set -e

DB_HOST=${DB_HOST:-db}
DB_PORT=${DB_PORT:-5432}

echo "Waiting for database at $DB_HOST:$DB_PORT..."
until nc -z "$DB_HOST" "$DB_PORT"; do
     echo "Waiting for DB..."
     sleep 1
done
echo "Database is up - continuing"

# Run migrations (noinput for automation)
python manage.py migrate --noinput

# Start the server (the CMD from Dockerfile will be appended here)
exec "$@"