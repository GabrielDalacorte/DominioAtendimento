import json
import requests
from payment_receipt import const


class WsGetToken:

    def __init__(self):
        self.__token = None
        pass

    def get_token(self):

        if self.__token is None:
            params = {
                'username': const.USERNAME_LOGIN,
                'password': const.PASSWORD_LOGIN
            }
            key = requests.post(const.URL_LOGIN, data=params)

            key_headers = json.loads(key.text)
            self.__token = key_headers

        return self.__token