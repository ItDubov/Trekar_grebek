import os
import telegram
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telegram.Bot(token=BOT_TOKEN)

def send_message(chat_id: str, text: str):
    """
    Отправка сообщения пользователю
    """
    try:
        bot.send_message(chat_id=chat_id, text=text)
    except Exception as e:
        print(f"Ошибка отправки сообщения: {e}")
        