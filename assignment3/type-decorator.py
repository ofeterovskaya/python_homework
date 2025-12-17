# type-decorator.py
from functools import wraps

def type_decorator(type_of_output):
    """
    Decorator factory: takes a type (str/int/float),
    and returns a decorator that converts the RESULT of the function to this type.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            x = func(*args, **kwargs)   # call the original function
            return type_of_output(x)    # try to convert the result to the required type
        return wrapper
    return decorator


@type_decorator(str)
def return_int():
    # Return number 5, and the decorator converts it to string "5"
    return 5


@type_decorator(int)
def return_string():
    # Return string "not a number".
    # Decorator will try to do int("not a number") -> this will raise ValueError.
    return "not a number"


if __name__ == "__main__":
    y = return_int()
    print(type(y).__name__)  # should print: str

    try:
        y = return_string()
        print("shouldn't get here!")
    except ValueError:
        print("can't convert that string to an integer!")  # end up here
