from time import sleep

from config import QUEUE_ID, QUEUE_NAME, KEYWORD, PAUSE
from telegram import send_message
from connections import get_client
from tickets import TicketManager
from killer import PerfectKiller


manager = TicketManager(get_client(), QUEUE_ID, KEYWORD)
manager.queue_name = QUEUE_NAME
killer = PerfectKiller()


# Уведомляем о начале работы
send_message(manager.get_start_message())

# "Event" loop
while not killer.kill_now:

    # Получаем тикеты
    manager.get_new_tickets()

    if killer.kill_now:
        break

    # Проверяем актуальность имеющихся тикетов
    manager.check_exist_ticket_in_otrs()

    if killer.kill_now:
        break

    # Итерируемся по имеющимся тикетам
    for tic in manager.exist_tickets:

        message = manager.check_exist_ticket(tic)

        if message:
            send_message(message)

        if killer.kill_now:
            break

    if killer.kill_now:
        break

    # Итерируемся по важным тикетам
    for tic in manager.important_tickets:

        message = manager.check_important_ticket(tic)

        send_message(message)

        if killer.kill_now:
            break

    for sec in range(PAUSE - 1):

        sleep(1)

        if killer.kill_now:
            break

# Уведомление о завершении работы
send_message(f'Получен сигнал {killer.signal}, выходим.')

# Выходим красиво
killer.perfect_exit()
