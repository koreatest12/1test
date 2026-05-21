#!/usr/bin/env bash
set -euo pipefail

export DJANGO_SETTINGS_MODULE=config.settings
python manage.py migrate --noinput
python manage.py runserver 0.0.0.0:8000
