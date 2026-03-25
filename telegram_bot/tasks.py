from celery import shared_task
from django.utils import timezone
from habits.models import Habit
from .bot import send_message

@shared_task
def send_habit_reminders():
    """
    Задача, которая проверяет все привычки и отправляет напоминания
    """
    now = timezone.now()
    habits = Habit.objects.filter(is_active=True)  # только активные привычки
    for habit in habits:
        # Проверяем, пора ли напомнить
        if habit.time_to_remind():  # метод модели Habit, который проверяет время
            if habit.user.telegram_id:
                send_message(
                    chat_id=habit.user.telegram_id,
                    text=f"Напоминание: {habit.action} в {habit.place} в {habit.time}"
                )
