import threading

from typing import Callable


def set_interval(interval: int) -> Callable:
    """
    Periodic execution
    :param interval: In seconds
    :type interval: int
    :return:
    :rtype:
    """

    def wrapper(func):
        """Wrapper function for periodic caller"""

        def wrapped(*args, **kwargs):
            stopped = threading.Event()

            def worker():
                while not stopped.wait(interval):
                    func(*args, **kwargs)

            threading.Thread(target=worker, daemon=True).start()
            return stopped

        return wrapped

    return wrapper
