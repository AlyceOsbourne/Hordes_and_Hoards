# decorator to time functions
from functools import wraps


def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        import time
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:2f} seconds")
        return result

    return wrapper

