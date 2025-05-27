#!/usr/bin/env bash
# build.sh

# Применяем миграции
python manage.py migrate

# Собираем статику
python manage.py collectstatic --noinput
