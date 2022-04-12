def fromDate(dt: str):
    # YYYY-MM-DD
    year = dt[2:4]
    month = dt[5:7]
    day = dt[8:]
    print(year, month, day)
    return '{:08b}'.format(int(year)) + ' ' + '{:08b}'.format(int(month)) + ' ' + '{:08b}'.format(int(day))


def fromInt(dt: int):
    return bytes(dt)


def fromFloat(dt: float):
    return bytes(dt)
