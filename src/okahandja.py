import struct

from .text import padLeft


def formatName(filePath: str):
    """
    Rename a given file to the alphabetical version.
    
    eg 'okahandja_2021_3_7.*' becomes 'okh_2021_03_07.*'.
    """
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
    """Convert 24 bytes into their counter-part plaintext."""
    if len(data) < 24:
        return None

    _ints = [str(int(x)) for x in data]

    DATE = f'20{padLeft(_ints[0])}-{padLeft(_ints[1])}-{padLeft(_ints[2])}'
    TIME = f'{padLeft(_ints[3])}:{padLeft(_ints[4])}:{padLeft(_ints[5])}'

    HUM = fromArr(_ints[6:8])
    AMB = fromArr(_ints[8:10])
    SYS = fromArr(_ints[10:12])
    PVT = fromArr(_ints[12:14])
    V3 = fromArr(_ints[14:16])
    PVC = fromBigArr(data[16:20])
    V12 = fromArr(_ints[20:22])

    return f'{DATE},{TIME},{HUM},{AMB},{SYS},{PVT},{V3},{PVC},{V12}\n'

def getDateFromBytes(data: bytes) -> str:
    """Extract the date string from a bytecoded record in the format: YYYY-MM-DD."""
    if len(data) < 3:
        return None

    _ints = [str(int(x)) for x in data]
    
    return f'20{padLeft(_ints[0])}-{padLeft(_ints[1])}-{padLeft(_ints[2])}'


def getTimeFromBytes(data: bytes) -> str:
    """Extract the time string from a bytecoded record in the format: HH:MM:SS."""
    if len(data) < 6:
        return None

    _ints = [str(int(x)) for x in data]

    return f'{padLeft(_ints[3])}:{padLeft(_ints[4])}:{padLeft(_ints[5])}'



def getTimeValueFromBytes(data: bytes) -> int:
    """Extract the time value from a bytecoded record in the format: HHMMSS."""
    if len(data) < 6:
        return None

    _ints = [str(int(x)) for x in data]

    return int(f'{padLeft(_ints[3])}{padLeft(_ints[4])}{padLeft(_ints[5])}')