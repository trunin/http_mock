from time import sleep
from datetime import datetime, timedelta


def wait(func, timeout_sec: float):
    expiration_time = datetime.now() + timedelta(seconds=timeout_sec)
    while True:
        res = func()
        if res is not None:
            return res
        now = datetime.now()
        if now > expiration_time:
            return None
        sleep(0.2)