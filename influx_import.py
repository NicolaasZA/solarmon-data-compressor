import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.client.write_api import WriteType, WriteOptions, Point

from src.files import fileToLines, filesToLines, getFileList

def convertToPoint(recordCSV: str, hostTag: str = None):

    if recordCSV.startswith('DATE'):
        return None

    parts = recordCSV.split(',')

    timestamp = f'{parts[0]}T{parts[1]}+0200'

    if hostTag is None:
        hostTag = 'oka01'

    return Point('okahandja') \
        .time(timestamp) \
        .tag('host', hostTag) \
        .field('HUM', float(parts[2])) \
        .field('AMB', float(parts[3])) \
        .field('SYS', float(parts[4])) \
        .field('PVT', float(parts[5])) \
        .field('V3', float(parts[6])) \
        .field('PVC', float(parts[7])) \
        .field('V12', float(parts[8]))


# Change the following to aim at your database.
BUCKET = 'okahandja'
ORG = 'solarmon'
TOKEN = '9sd7uIu2DL0M5o2Er-wnD-vvHUKTjOR4zHD66adFYSMgx3kyJBfsZ745PCS2By9IglF5_eiIY6ukw3p-WTxrDQ=='
URL = 'http://localhost:8086'
HOSTTAG = 'oka01'


print('Configuring...')
files = getFileList('compressed/csv/', 'csv')
client = influxdb_client.InfluxDBClient(
    url=URL,
    token=TOKEN,
    org=ORG
)
write_api = client.write_api(write_options=WriteOptions(batch_size=500, flush_interval=5000))

print('Wiping bucket...')
c = client.delete_api()
c.delete(start='1900-01-01T00:00:00Z', stop='2030-12-31T23:59:00Z', predicate='host="' + HOSTTAG + '"', bucket=BUCKET)


print(f'Processing {len(files)} files...')
for f in files:
    csv = fileToLines(f)
    records = []

    for line in csv:
        v = convertToPoint(line, HOSTTAG)
        if v is not None:
            records.append(v)

    print(f'Writing {len(records)} entries for {f}')
    for rec in records:
        write_api.write(BUCKET, record=rec)

print('Flushing')
write_api.flush()
write_api.close()

print('Done')
