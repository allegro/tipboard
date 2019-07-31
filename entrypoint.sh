#!/usr/bin/env bash
nohup redis-server &
python manage.py runserver 0.0.0.0:8080 --noreload