import os

from dotenv import load_dotenv

load_dotenv()

OTRS_HOST = os.getenv('OTRS_HOST')
USER_NAME = os.getenv('USER_NAME')
PASSWORD = os.getenv('PASSWORD')
PAUSE = int(os.getenv('PAUSE'))

QUEUE_ID = int(os.getenv('QUEUE_ID'))
QUEUE_NAME = os.getenv('QUEUE_NAME')
KEYWORD = os.getenv('KEYWORD')

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_MY_CHAT_ID = os.getenv('TELEGRAM_MY_CHAT_ID')
