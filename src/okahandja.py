import struct


def toArr(val: str):
    parts = val.split('.')
    second = parts[1][:2] if len(parts[1]) > 2 else parts[1]
    return [int(parts[0]), int(second)]


def toBigArr(val: str):
    return [int(x) for x in struct.pack("f", float(val))]


def lineToBytes(line: str) -> bytes:
    if line.startswith('DATE') or line.count(',') != 8:
        return None

    line = line.removesuffix('\n')

    DATE, TIME, HUM, AMB, SYS, PVT, V3, PVC, V12 = line.split(',')

    dates = [int(DATE[2:4]), int(DATE[5:7]), int(DATE[8:]),
             int(TIME[:2]), int(TIME[3:5]), int(TIME[6:])]

    hum_b = toArr(HUM)
    amb_b = toArr(AMB)
    sys_b = toArr(SYS)
    pvt_b = toArr(PVT)
    v3_b = toArr(V3)
    pvc_b = toBigArr(PVC)
    v12_b = toArr(V12)

    try:
        return bytes(dates + hum_b + amb_b + sys_b + pvt_b + v3_b + pvc_b + v12_b + [10, 10])
    except:
        print(dates, hum_b, amb_b, sys_b, pvt_b, v3_b, pvc_b, v12_b)
        return None
