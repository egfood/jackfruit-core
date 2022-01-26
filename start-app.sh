#!/bin/sh
./manage.py migrate
./manage.py createsuperuser --noinput
daphne -b 0.0.0.0 -p $PORT core.asgi:application
