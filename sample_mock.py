from flask import request

from http_mock import HttpMock


class SampleMock(HttpMock):
    _get_users_path = '/api/v1/user'
    _get_user_path = '/api/v1/user/<int:user_id>'

    def __init__(self, host: str = None, port: str = None):
        super().__init__(host, port)

        """ data """
        self._users = {}

        """ routes """
        self._add_route('get_users', 'GET', self._get_users_path, self._get_users_handler())

    def add_user(self, shop: dict):
        self._users[shop['id']] = shop

    def _get_users_handler(self):
        if request not in self._requests:
            self._requests.append(request)
        return self._users

    def wait_for_request_by_id(self, user_id: int, timeout_sec: int = 2):
        def filter_func(req):
            id_val = req.json['id'] if 'id' in req.json else None
            return id_val == user_id

        return self.wait_for_request(filter_func, timeout_sec)
