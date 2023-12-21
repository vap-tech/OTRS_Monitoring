import time

from pyotrs import Client, Ticket


class TicketManager:

    def __init__(
            self,
            otrs_client: Client,
            otrs_queue_id: int,
            keyword: str
    ):
        self.client = otrs_client
        self.client.session_create()
        self.queue_id = otrs_queue_id
        self.queue_name = None
        self.keyword = keyword.lower()
        self.tickets_in_otrs = []
        self.exist_tickets = []
        self.important_tickets = []

    def __repr__(self):

        _str = f"""
        Всего тикетов: {len(self.exist_tickets)}\n
        Важных: {len(self.important_tickets)}
        """

        return _str

    def get_start_message(self):

        return f'Запущен мониторинг очереди {self.queue_name}'

    @staticmethod
    def _get_message_for_ticket(_ticket: Ticket) -> str:

        _ticket_number: str = _ticket.fields['TicketNumber']
        _title: str = _ticket.fields['Title']
        _title = _title.replace('#', ' ')
        _state: str = _ticket.fields['State']
        _owner: str = _ticket.fields['Owner']

        message = f'''{_ticket_number}
        Тема: {_title}
        Состояние: {_state}
        Владелец: {_owner}\n'''

        return message

    @staticmethod
    def get_article_for_ticket(_ticket: Ticket) -> str:

        _message = _ticket.articles[-1].fields['Body']
        message = 'Сообщение: ' + _message

        return message

    def get_new_tickets(self):

        """
        Получает тикеты из OTRS и дополняет exist_tickets теми тикетами,
        которых не было в exist_tickets.
        :return: None
        """

        try:
            self.tickets_in_otrs = self.client.ticket_search(
                States=['new'],
                QueueIDs=[self.queue_id]
            )

        except Exception as err:
            print(f'error: {err}')
            time.sleep(10)
            self.client.session_create()
            self.get_new_tickets()

        finally:
            for _ticket in self.tickets_in_otrs:
                if _ticket in self.exist_tickets:
                    continue
                self.exist_tickets.append(_ticket)

            self.tickets_in_otrs.clear()

    def check_exist_ticket_in_otrs(self):

        """
        Проверяет тикеты из exist_tickets на присутствие в OTRS,
        если тикет отсутствует в OTRS, он удаляется и в exist_tickets.
        :return: None
        """

        try:
            self.tickets_in_otrs = self.client.ticket_search(
                States=['new'],
                QueueIDs=[self.queue_id]
            )

        except Exception as err:
            print(f'error: {err}')
            time.sleep(10)
            self.client.session_create()
            self.check_exist_ticket_in_otrs()

        finally:
            for _ticket in self.exist_tickets:
                if _ticket in self.tickets_in_otrs:
                    continue
                self.exist_tickets.remove(_ticket)

            self.tickets_in_otrs.clear()

    def check_exist_ticket(self, _ticket_id: str):

        """
        Проверяет тему тикета на ключевое слово,
        в случае совпадения добавляет тикет в important_tickets,
        удаляет его из new_tickets и генерирует сообщение о новом тикете.
        Возвращает None если совпадения не было.
        :param _ticket_id:
        :return: Сообщение о новом тикете или None
        """

        if _ticket_id in self.important_tickets:
            return

        _ticket = None

        try:
            _ticket = self.client.ticket_get_by_id(int(_ticket_id))

        except Exception as err:
            print(f'error: {err}')
            self.check_exist_ticket(_ticket_id)

        _title: str = _ticket.fields['Title']

        if self.keyword in _title.lower():
            self.important_tickets.append(_ticket_id)
            self.exist_tickets.remove(_ticket_id)

            _message = f'Новый тикет в очереди {self.queue_name}: '
            _message += self._get_message_for_ticket(_ticket)

            return _message

    def check_important_ticket(self, _ticket_id: str):

        """
        Проверяет важный тикет. В зависимости от его статуса
        возвращает сообщение о том, что тикет не обработан/обработан
        или с ним что-то не так. В зависимости от статуса может удалить
        тикет из important_tickets.
        :param _ticket_id: Id тикета
        :return: Сообщение для отправки
        """

        _ticket = None

        try:
            _ticket = self.client.ticket_get_by_id(int(_ticket_id), articles=True)
        except Exception as err:
            print(f'error: {err}')
            self.check_important_ticket(_ticket_id)

        _state: str = _ticket.fields['State']
        _queue_id: str = _ticket.fields['QueueID']

        _message = None

        if _queue_id != self.queue_id:

            _message = f"Тикет в очереди {self.queue_name} перемещён: "
            _message += self._get_message_for_ticket(_ticket)
            _message += self.get_article_for_ticket(_ticket)

            self.important_tickets.remove(_ticket_id)

        elif _state == 'new':

            _message = f"Тикет в очереди {self.queue_name} без ответа!: "
            _message += self._get_message_for_ticket(_ticket)
            _message += self.get_article_for_ticket(_ticket)

        elif 'resolved' in _state:

            _message = f"Тикет в очереди {self.queue_name} resolved!: "
            _message += self._get_message_for_ticket(_ticket)
            _message += self.get_article_for_ticket(_ticket)

            self.important_tickets.remove(_ticket_id)

        elif 'open' in _state:

            _message = f"Тикет в очереди {self.queue_name} обработан: "
            _message += self._get_message_for_ticket(_ticket)
            _message += self.get_article_for_ticket(_ticket)

            self.important_tickets.remove(_ticket_id)

        return _message
