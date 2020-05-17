from multiprocessing import Process
from flask import Flask
from helpers.localhost import get_local_host
from helpers.wait import wait


class HttpMock:

    def __init__(self, host: str = None, port: str = None):
        self._app = Flask(__name__)
        self._host = host or get_local_host()
        self._port = port or '8080'
        self._requests = []

    def start(self):
        """ start mock process """
        self._mock = Process(target=self._app.run(host=self._host,
                                                  port=self._port))
        self._mock.start()

    def stop(self):
        """ terminate mock process """
        self._mock.terminate()

    def _add_route(self, rule, method: str, path: str, handler):
        """ routes factory method """
        self._app.add_url_rule(path, endpoint=rule, view_func=handler, methods=[method])

    def get_all_requests(self):
        return self._requests

    def wait_for_request(self, filter_func=None, timeout_sec: int = 2):
        def func():
            if filter_func is not None:
                req = next((req for req in self._requests if filter_func(req) is True), None)
            else:
                req = next((req for req in self._requests), None)
            return req
        return wait(func, timeout_sec)
