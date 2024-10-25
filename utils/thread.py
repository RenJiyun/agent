import threading
import time

def entry_handler(func):
    def wrapper(*args, **kwargs):
        threading.local().start_time = time.time()
        result = func(*args, **kwargs)
        delattr(threading.local(), "start_time")
        return result
    return wrapper


def check_timeout(timeout):
    if time.time() - threading.local().start_time > timeout:
        raise TimeoutError("The operation has timed out")


def get_remaining_time(timeout):
    return timeout - (time.time() - threading.local().start_time)


