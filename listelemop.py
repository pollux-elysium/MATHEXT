def mul(x: list, y: list):
    return [i*j for i, j in zip(x, y)]


def div(x: list, y: list):
    return [i/j for i, j in zip(x, y)]


def add(x: list, y: list):
    return [i+j for i, j in zip(x, y)]


def sub(x: list, y: list):
    return [i-j for i, j in zip(x, y)]