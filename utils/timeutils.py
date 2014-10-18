from functools import wraps
import errno
import os
import signal
import pytz


class TimeoutError(Exception):
    pass


def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator


def set_time_zones(posts):
    utc = pytz.utc

    posts_new = posts
    for p in posts_new:
        p.saved_date = utc.localize(p.saved_date)
    return posts_new
