from .typedef import *

def mul(x: list[number], y: list[number]) -> list[number]:
    return [i*j for i, j in zip(x, y)]


def div(x: list[number], y: list[number]) -> list[float]:
    return [i/j for i, j in zip(x, y)]


def add(x: list[number], y: list[number]) -> list[number]:
    return [i+j for i, j in zip(x, y)]


def sub(x: list[number], y: list[number]) -> list[number]:
    return [i-j for i, j in zip(x, y)]