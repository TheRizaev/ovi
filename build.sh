#!/usr/bin/env bash
# build.sh

set -o errexit  # Exit on error

# Установка зависимостей
pip install -r requirements.txt

# Сбор статических файлов
python manage.py collectstatic --noinput

# Применение миграций
python manage.py migrate

# Создание тестовых данных (если необходимо)
python manage.py create_test_data
