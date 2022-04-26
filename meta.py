from dateutil import parser
import glob
import json
from src.files import fileToBytes
from src.okahandja import bytesToRecordObject

EXT_IN = '.dat'
FOLDER_IN = 'compressed/dat/'
PATH_OUT = 'compressed/meta.json'

LINE_BYTES_SIZE = 24

files = glob.glob(FOLDER_IN + '*' + EXT_IN)

fileStats = []
for datPath in files:
    dateString = datPath.replace(EXT_IN, '').replace(
        FOLDER_IN, '').replace('okh_', '').replace('_', '-')
    stamp = parser.parse(f'{dateString}T12:00:00+0200').timestamp()

    entry = {
        'HUM': {'min': 100, 'max': 0, 'avg': 0, 'total': 0, 'minTime': '', 'maxTime': ''},
        'AMB': {'min': 100, 'max': 0, 'avg': 0, 'total': 0, 'minTime': '', 'maxTime': ''},
        'SYS': {'min': 100, 'max': 0, 'avg': 0, 'total': 0, 'minTime': '', 'maxTime': ''},
        'PVT': {'min': 100, 'max': 0, 'avg': 0, 'total': 0, 'minTime': '', 'maxTime': ''},
        'PVC': {'min': 100, 'max': 0, 'avg': 0, 'total': 0, 'minTime': '', 'maxTime': ''},
    }
    ekeys = entry.keys()
    recordCount = 0

    # Read data from file
    data = fileToBytes(datPath)
    start = 0
    while start < len(data):
        line = data[start:start+24]
        record = bytesToRecordObject(line)

        for field in ekeys:
            entry[field]['total'] += float(record[field])

            

            if float(record[field]) < entry[field]['min']:
                entry[field]['minTime'] = record['TIME']
                entry[field]['min'] = float(record[field])

            if float(record[field]) > entry[field]['max']:
                entry[field]['maxTime'] = record['TIME']
                entry[field]['max'] = float(record[field])

        recordCount += 1
        start += 24

    # Generate average
    for field in ekeys:
        entry[field]['avg'] = entry[field]['total'] / recordCount
        entry[field]['min'] = round(entry[field]['min'], 2)
        entry[field]['max'] = round(entry[field]['max'], 2)
        entry[field]['avg'] = round(entry[field]['avg'], 2)
        del entry[field]['total']

    # Add to buffer
    fileStats.append({
        'date': dateString,
        'stamp': stamp,
        'values': entry
    })

    print(f'Processed {datPath}')

meta = {
    'projectName': 'Okahandja',
    'files': sorted(fileStats, key=lambda d: d['stamp'])
}

with open(PATH_OUT, 'w') as out:
    out.writelines(json.dumps(meta))

print('done')
