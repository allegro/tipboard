#!/usr/bin/env bash
nohup redis-server --protected-mode no &
python src/manage.py runserver 0.0.0.0:8080 --noreload