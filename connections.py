from pyotrs import Client

from config import OTRS_HOST, USER_NAME, PASSWORD


client = Client(OTRS_HOST, USER_NAME, PASSWORD)


def get_client() -> Client:
    client.session_create()
    return client
