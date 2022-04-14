from dateutil import parser
import glob
import json
import os.path as path

EXT_HEX_IN = '.hex'
EXT_CSV_IN = '.csv'
FOLDER_HEX_IN = 'compressed/hex/'
FOLDER_CSV_IN = 'compressed/csv/'

LINE_BYTES_SIZE = 24
OUT_PATH = 'compressed/stats.json'

files = glob.glob(FOLDER_HEX_IN + '*')

fileStats = []
for hexPath in files:
    csvPath: str = hexPath.replace(FOLDER_HEX_IN, FOLDER_CSV_IN).replace(EXT_HEX_IN, EXT_CSV_IN)
    dateString = hexPath.replace(EXT_HEX_IN, '').replace(FOLDER_HEX_IN, '').replace('okh_', '').replace('_', '-')
    stamp = parser.parse(f'{dateString}T12:00:00+0200').timestamp()

    try:
        hexSize = path.getsize(hexPath)
        rowCount = int(hexSize / LINE_BYTES_SIZE)
    except:
        hexSize = 0
        rowCount = 0

    try:
        csvSize = path.getsize(csvPath)
    except:
        csvSize = 0

    fileStats.append({
        'date': dateString,
        'stamp': stamp,
        'records': rowCount,
        'csv': {
            'path': csvPath.replace(FOLDER_HEX_IN, 'hex/'),
            'size': csvSize
        },
        'hex': {
            'path': hexPath.replace(FOLDER_CSV_IN, 'csv/'),
            'size': hexSize
        }
    })

stats = {
    'projectName': 'Okahandja',
    'recordTarget': 8640,
    'files': sorted(fileStats, key=lambda d: d['stamp'])
}

with open(OUT_PATH, 'w') as out:
    out.writelines(json.dumps(stats))

print('done')
