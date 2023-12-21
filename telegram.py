import requests
from config import TELEGRAM_BOT_TOKEN as TOKEN, TELEGRAM_MY_CHAT_ID as CHAT_ID


def send_message(text: str, chat_id=CHAT_ID) -> None:

    """
    Отправляет через BOT API сообщение в telegram.
    По умолчанию адресата берёт из .env
    :param text: Текст сообщения
    :param chat_id: Адресат
    :return: None
    """

    requests.get(f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={text}')
