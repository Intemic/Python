def check_logged_in(func) -> object:
    def wrapper() -> str:
        if 'logged_in' in session:
            return func()
        else:
            return 'Вы НЕ в системе'
    return wrapper
