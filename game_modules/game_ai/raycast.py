import math


def cast_ray(position, angle, map):
    x, y = position
    dx, dy = math.cos(angle), math.sin(angle)
    while True:
        x += dx
        y += dy
        if x < 0 or x >= len(map[0]) or y < 0 or y >= len(map):
            return None
        if map[int(y)][int(x)]:
            return x, y


def cast_rays(position, angles, map):
    for angle in angles:
        obstacle = cast_ray(position, angle, map)
        if obstacle:
            return obstacle
    return None


def cast_ray_hit(position, target, map):
    x, y = position
    dx, dy = target[0] - x, target[1] - y
    if dx == 0 and dy == 0:
        return True
    if dx == 0:
        dy = dy / abs(dy)
    elif dy == 0:
        dx = dx / abs(dx)
    else:
        dx, dy = dx / abs(dx), dy / abs(dy)
    while True:
        x += dx
        y += dy
        if x < 0 or x >= len(map[0]) or y < 0 or y >= len(map):
            return False
        if map[int(y)][int(x)]:
            return True
