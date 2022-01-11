#!/bin/sh
./manage.py migrate
django-admin loaddata core/initial_user.json
daphne -b 0.0.0.0 -p $PORT core.asgi:application
