#!/bin/sh

MANAGE_DIR="/srv"
MAKEMIGRATIONS=false

usage(){
    echo ""
    echo "./reset_migrations.sh"
    echo "\t-h --help"
    echo "\t--makemigrations, if you need to create migrations"
    echo ""
}

error_exit() {
    echo "$1" 1>&2
    exit 1
}

while [ "$1" != "" ]; do
    PARAM=`echo $1 | awk -F= '{print $1}'`
    VALUE=`echo $1 | awk -F= '{print $2}'`
    case $PARAM in
        -h | --help)
            usage
            exit
            ;;
        --makemigrations)
            MAKEMIGRATIONS=true
            ;;
        *)
            echo "ERROR: unknown parameter \"$PARAM\""
            usage
            exit 1
            ;;
    esac
    shift
done

echo "Starting ..."

echo ">> Deleting database migrations..."
echo "DELETE FROM django_migrations;" | python $MANAGE_DIR/manage.py dbshell
echo ">> Done"

if [ "$MAKEMIGRATIONS" = true ] ; then
    echo ">> Erase all migrations..."
    find $MANAGE_DIR -path "*/migrations/*.py" -not -name "__init__.py" -delete
    find $MANAGE_DIR -path "*/migrations/*.pyc"  -delete
    echo ">> Done"

    echo ">> Making migrations..."
    python $MANAGE_DIR/manage.py makemigrations || error_exit "Cannot make migrations! Aborting"
    echo ">> Done"
fi

echo ">> Resetting the migrations for the 'built-in' apps..."
python $MANAGE_DIR/manage.py migrate --fake || error_exit "Cannot reset migrations! Aborting"
echo ">> Done"

echo ">> Migrating contenttypes..."
python $MANAGE_DIR/manage.py migrate contenttypes || error_exit "Cannot make migrations! Aborting"
echo ">> Done"

echo ">> Faking migrations..."
# replace --fake-initial with --fake to make it work for Django 1.9
python $MANAGE_DIR/manage.py migrate --fake-initial || error_exit "Cannot fake migrations! Aborting"
echo ">> Done"

echo ">> Migrating..."
python $MANAGE_DIR/manage.py migrate || error_exit "Almost done... or not :("
echo ">> Done"

echo "All done!"
