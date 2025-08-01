def ceildiv(a: int, b: int) -> int:
    """
    Finds the ceiling of a/b using upside-down floor division
    """
    return -(a // -b)
