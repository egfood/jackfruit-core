#!/bin/sh
./manage.py migrate
daphne -b 0.0.0.0 -p $PORT core.asgi:application
