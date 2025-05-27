#!/usr/bin/env bash
# build.sh

set -o errexit  # Exit on error

echo "Starting build process..."

# Установка зависимостей
echo "Installing dependencies..."
pip install -r requirements.txt

# Проверяем наличие статических файлов
echo "Checking static files..."
ls -la static/
echo "CSS files:"
ls -la static/css/ || echo "CSS directory not found"
echo "JS files:"
ls -la static/js/ || echo "JS directory not found"
echo "Icons:"
ls -la static/icons/ || echo "Icons directory not found"

# Очистка старых статических файлов
echo "Cleaning old static files..."
rm -rf staticfiles/*

# Сбор статических файлов с подробным выводом
echo "Collecting static files..."
python manage.py collectstatic --noinput --verbosity=2

# Проверяем что файлы скопировались
echo "Checking collected static files..."
ls -la staticfiles/
echo "Collected CSS files:"
ls -la staticfiles/css/ || echo "No CSS files collected"

# Применение миграций
echo "Running migrations..."
python manage.py migrate

# Создание тестовых данных (если необходимо)
echo "Creating test data..."
python manage.py create_test_data || echo "Test data creation failed or command not found"

echo "Build completed successfully!"
