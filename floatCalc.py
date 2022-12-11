def nearZero(n:float,e:int=9) -> bool:
    """Check if a number is near zero

    Args:
        n (float): Number
        e (int, optional): Error in 10th power. Defaults to 9.

    Returns:
        bool: True if near zero
    """
    return round(n,e)==0 