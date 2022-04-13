import struct

from .text import padLeft


def formatName(filePath: str):
    # Receive: okahandja_2021_3_7.*
    # Return: okh_2021_03_07.*
    result = filePath.replace('okahandja', 'okh')

    # format month
    result = result.replace('_1_', '_01_').replace('_2_', '_02_').replace('_2_', '_02_')
    result = result.replace('_3_', '_03_').replace('_4_', '_04_').replace('_5_', '_05_')
    result = result.replace('_6_', '_06_').replace('_7_', '_07_').replace('_8_', '_08_').replace('_9_', '_09_')
    # format days
    result = result.replace('_1.', '_01.').replace('_2.', '_02.').replace('_2.', '_02.')
    result = result.replace('_3.', '_03.').replace('_4.', '_04.').replace('_5.', '_05.')
    result = result.replace('_6.', '_06.').replace('_7.', '_07.').replace('_8.', '_08.').replace('_9.', '_09.')
    return result

def fromArr(vals: list):
    return str(vals[0] + '.' + vals[1])


def toArr(val: str):
    parts = val.split('.')
    second = parts[1][:2] if len(parts[1]) > 2 else parts[1]
    return [int(parts[0]), int(second)]


def fromBigArr(vals: bytes):
    f_v = struct.unpack('<f', vals)[0]
    return "{:.1f}".format(f_v)


def toBigArr(val: str):
    return [int(x) for x in struct.pack("f", float(val))]


def lineToBytes(line: str) -> bytes:
    if line.startswith('DATE') or line.count(',') != 8:
        return None

    line = line.replace('\n', '')

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
        return bytes(dates + hum_b + amb_b + sys_b + pvt_b + v3_b + pvc_b + v12_b + [13, 10])
    except:
        return None


def bytesToLine(data: bytes) -> bytes:
    """Convert 22/24 bytes into their counter-part plaintext."""
    if len(data) < 22:
        print(data)
        return None

    as_int = [str(int(x)) for x in data]

    DATE = f'20{padLeft(as_int[0])}-{padLeft(as_int[1])}-{padLeft(as_int[2])}'
    TIME = f'{padLeft(as_int[3])}:{padLeft(as_int[4])}:{padLeft(as_int[5])}'

    HUM = fromArr(as_int[6:8])
    AMB = fromArr(as_int[8:10])
    SYS = fromArr(as_int[10:12])
    PVT = fromArr(as_int[12:14])
    V3 = fromArr(as_int[14:16])
    PVC = fromBigArr(data[16:20])
    V12 = fromArr(as_int[20:22])

    return f'{DATE},{TIME},{HUM},{AMB},{SYS},{PVT},{V3},{PVC},{V12}\n'

# 2022-04-04,23:57:20,53.6,17.5,42.8,11.4,3.31,0.0,14.3
# 2022-4-4,23:57:20,53.6,17.5,42.8,11.4,3.31,0.0,14.3
