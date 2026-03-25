# Habits Tracker Backend

## Установка
1. Создать виртуальное окружение: `python -m venv .venv`
2. Активировать его: `source .venv/Scripts/activate` (Windows) или `source .venv/bin/activate` (Linux/Mac)
3. Установить зависимости: `pip install -r requirements.txt`
4. Настроить `.env` с SECRET_KEY, DB_*, REDIS_URL, TELEGRAM_TOKEN
5. Миграции: `python manage.py makemigrations && python manage.py migrate`
6. Запуск сервера: `python manage.py runserver`
7. Celery: `celery -A config worker -l info`
8. Redis должен быть запущен