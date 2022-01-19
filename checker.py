from flask import session
from functools import wraps


def check_logged_in(func) -> object:
    @wraps(func)
    def wrapper(*args, **kwargs) -> str:
        if 'logged_in' in session:
            return func(*args, **kwargs)
        else:
            return 'Вы НЕ в системе'

    return wrapper
