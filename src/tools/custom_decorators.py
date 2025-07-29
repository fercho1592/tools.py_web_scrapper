import time

def delayed_view_timer(func):
    def wrapper(*args, **kwargs):
        time.sleep(5)
        return func(*args, **kwargs)
    return wrapper
