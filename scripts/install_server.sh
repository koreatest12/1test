#!/usr/bin/env bash
set -euo pipefail

python -m pip install --upgrade pip setuptools wheel
pip install -r requirements-ci.txt
python manage.py migrate --noinput
python manage.py collectstatic --noinput || true
python manage.py check
