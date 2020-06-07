"""
Custom decorators
"""

import time
import logging
from functools import wraps
from typing import Tuple, Callable


def restartable(max_attempts: int = 5,
                delay: int = 0.5,
                backoff: int = 2,
                exceptions: Tuple[Exception] = (Exception,),
                callback: Callable = None):
    """
    Wraps function with a try-except, making it restartable.

    :param max_attempts: max attempts count
    :param delay: seconds to sleep after first attempt
    :param backoff: multiplier for delay between attempts
    :param exceptions: list of exceptions to catch
    :param callback: func to call after exception

    :return: func value or raise exception (if error)
    """

    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = max_attempts
            to_sleep = delay
            last_ex = None

            while attempts > 0:
                try:
                    return func(*args, **kwargs)
                except exceptions as ex:
                    last_ex = ex
                    msg = "Sleep to {sec} sec. Func - {f}. Exception - {ex}"
                    logging.info(msg.format(
                        f=func.__name__,
                        ex=ex,
                        sec=to_sleep
                    ))
                    if callback:
                        callback()

                    time.sleep(to_sleep)
                    to_sleep *= backoff
                    attempts -= 1

            raise last_ex

        return wrapper

    return decorate
