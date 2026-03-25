import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# Периодические задачи
from celery.schedules import crontab

app.conf.beat_schedule = {
    "send-habit-reminders-every-5-min": {
        "task": "telegram_bot.tasks.send_habit_reminders",
        "schedule": crontab(minute="*/5"),  # каждые 5 минут
    },
}

app.conf.timezone = "UTC"
