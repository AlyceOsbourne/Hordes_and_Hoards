def bounded(val, minimum, maximum):
    return min(max(val, minimum), maximum)


def all_are_within_bounds(iterable, minimum, maximum):
    return all(map(lambda x: bounded(x, minimum, maximum), iterable))


def any_within_bounds(iterable, minimum, maximum):
    return any(map(lambda x: minimum < x <= maximum, iterable))


def get_all_in_bounds(iterable, minimum, maximum):
    return [i for i in iterable if minimum < i <= maximum]
