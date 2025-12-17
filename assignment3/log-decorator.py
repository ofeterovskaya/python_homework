import logging
from functools import wraps

# One-time logger setup
logger = logging.getLogger(__name__ + "_parameter_log")
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler("./decorator.log", "a"))

def logger_decorator(func):
    """Logs function name, positional/keyword params, and return value to ./decorator.log"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        pos = list(args) if args else "none"
        kw = dict(kwargs) if kwargs else "none"
        logger.info(f"function: {func_name}")
        logger.info(f"positional parameters: {pos}")
        logger.info(f"keyword parameters: {kw}")
        result = func(*args, **kwargs)
        logger.info(f"return: {result}")
        return result
    return wrapper

# 1) No-parameter, returns nothing
@logger_decorator
def say_hello():
    print("Hello, World!")

# 2) Variable number of positional args, returns True
@logger_decorator
def all_positional(*args):
    return True

# 3) No positional args, variable keyword args, returns logger_decorator
@logger_decorator
def only_keywords(**kwargs):
    return logger_decorator

if __name__ == "__main__":
    say_hello()
    all_positional(1, "two", 3.0, [4])
    only_keywords(a=1, b="bee", active=True)
