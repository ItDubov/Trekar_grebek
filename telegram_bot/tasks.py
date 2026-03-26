from celery import shared_task
from django.utils import timezone
from habits.models import Habit
from .bot import send_message


@shared_task
def send_habit_reminders():
    """
    Проверяет привычки и отправляет напоминания
    """
    habits = Habit.objects.filter(is_active=True)

    for habit in habits:
        if habit.time_to_remind():
            if habit.user.telegram_id:
                send_message(
                    chat_id=habit.user.telegram_id,
                    text=f"Напоминание: {habit.action} в {habit.place} в {habit.time}"
                )
