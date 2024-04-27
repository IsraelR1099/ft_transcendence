#!/bin/sh

# Check if the database is using PostgreSQL
if [ "$DBASE" = "postgreSQL" ]
then
    # Wait for the database to be ready
    # This is necessary because the database container may not be ready to accept connections when the web container starts
    echo "Waiting for the database to be ready..."
	/usr/local/bin/wait-for-it.sh $POSTGRES_HOST:$POSTGRES_PORT -t 0
    echo "Database ready"
fi

# Check if any migrations are applied
if [ "$(ls /srv/user/migrations/000*.py 2>/dev/null | wc -l)" -eq 0 ];
then
	# No migrations are applied so we run migrations and migrate
	echo "No migrations applied. Running migrations..."
	# Apply database migrations
	python manage.py makemigrations
	python manage.py migrate
	echo "Migrations applied."
else
	echo "Migrations already applied."
	# Check if reset_migrations is requested
	if [ "$RESET_MIGRATIONS" = "true" ]
	then
		echo "Resetting migrations..."
		/usr/local/bin/reset_migrations.sh --makemigrations
		echo "Migrations reset."
	fi
fi

# Run the server
python manage.py runserver 0.0.0.0:8000 2>&1
daphne -u /tmp/daphne.sock transcendance.asgi:application

exec "$@"
