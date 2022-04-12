def padLeft(val: str, length=2, c='0'):
    """Left-pad a value to meet the desired length, using the specified character c."""
    if length <= len(val):
        return val
    needed = length - len(val)
    return (c * needed) + val


def padRight(val: str, length=2, c='0'):
    """Right-pad a value to meet the desired length, using the specified character c."""
    if length <= len(val):
        return val
    needed = length - len(val)
    return val + (c * needed)
