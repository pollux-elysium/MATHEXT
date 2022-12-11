from .typedef import *

def mul(x: list[number], y: list[number]) -> list[number]:
    """Multiply two lists element-wise
    
    Args:
        x (list[number]): First list
        y (list[number]): Second list
        
    Returns:
        list[number]: Result of element-wise multiplication
    """
    return [i*j for i, j in zip(x, y)]


def div(x: list[number], y: list[number]) -> list[float]:
    """Divide two lists element-wise

    Args:
        x (list[number]): First list
        y (list[number]): Second list

    Returns:
        list[float]: Result of element-wise division
    """
    return [i/j for i, j in zip(x, y)]


def add(x: list[number], y: list[number]) -> list[number]:
    """Add two lists element-wise

    Args:
        x (list[number]): First list
        y (list[number]): Second list

    Returns:
        list[number]: Result of element-wise addition
    """
    return [i+j for i, j in zip(x, y)]


def sub(x: list[number], y: list[number]) -> list[number]:
    """Subtract two lists element-wise

    Args:
        x (list[number]): First list
        y (list[number]): Second list

    Returns:
        list[number]: Result of element-wise subtraction
    """
    return [i-j for i, j in zip(x, y)]