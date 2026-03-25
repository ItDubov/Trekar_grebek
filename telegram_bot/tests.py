from django.test import TestCase
from telegram_bot.tasks import send_habit_reminders
from unittest.mock import patch

class CeleryTaskTest(TestCase):

    @patch("telegram_bot.tasks.bot.send_message")
    def test_send_reminder_task(self, mock_send):
        chat_id = 123456
        message = "Test Habit Reminder"
        send_habit_reminders(chat_id, message)
        mock_send.assert_called_once_with(chat_id=chat_id, text=message)
