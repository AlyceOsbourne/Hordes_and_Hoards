# decorator to time functions
import random
from functools import wraps

random_insults = [
    "You are a slowpoke",
    "Do better, dumbass",
    "You're not getting paid hourly, does it really need to take this long?",
    "Worthless!",
    "눈_눈",
    "┌∩┐(ಠ_ಠ)┌∩┐",
    "(╯°□°)╯︵ ┻━┻",
    "(⋟﹏⋞)",
    "┻━┻ ︵ヽ(`Д´)ﾉ︵┻━┻",
    "°ಠಿ●ಠಿ°",
    "ಠ_ಠ",
    "ಠoಠ",
    "ಠ⌣_ಠ",
    "ಠ益ಠ",
    "✖‿✖",
    "ಠ_ರೃ",
    "[{-_-}] ZZZzz zz z..."
]
random_compliments = [
    "You're a smart cookie",
    "Good job",
    "Keep up the hard work",
    "٩(ˊᗜˋ*)و",
    "＼（Ｔ∇Ｔ）／",
    "ヽ(´▽｀)ノ",
    "ѽ͜ (ᵔ ̮ ᵔ)›",
    "(๑>ᴗ<๑)",
    "(∩_∩)",
    "(❀◦‿◦)"
]


def time_it(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        import time
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:2f} seconds")
        return result

    return wrapper


def time_it_min(expected_time):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            import time
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            if end - start < expected_time:
                print(f"{func.__name__} took \033[92m{end - start:2f}\033[0m seconds, "
                      f"expected a maximum of {expected_time} seconds, {random.choice(random_compliments)}")
            else:
                # print in red
                print(f"{func.__name__} took \033[91m{end - start:2f}\033[0m seconds, "
                      f"expected a maximum of {expected_time} seconds, {random.choice(random_insults)}")
            return result

        return wrapper

    return decorator
