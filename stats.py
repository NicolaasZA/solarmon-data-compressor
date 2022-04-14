from dateutil import parser
import glob
import json
import os.path as path

EXT_DAT_IN = '.dat'
EXT_CSV_IN = '.csv'
FOLDER_DAT_IN = 'compressed/dat/'
FOLDER_CSV_IN = 'compressed/csv/'

LINE_BYTES_SIZE = 24
OUT_PATH = 'compressed/stats.json'

files = glob.glob(FOLDER_DAT_IN + '*')

fileStats = []
for datPath in files:
    csvPath: str = datPath.replace(FOLDER_DAT_IN, FOLDER_CSV_IN).replace(EXT_DAT_IN, EXT_CSV_IN)
    dateString = datPath.replace(EXT_DAT_IN, '').replace(FOLDER_DAT_IN, '').replace('okh_', '').replace('_', '-')
    stamp = parser.parse(f'{dateString}T12:00:00+0200').timestamp()

    try:
        datSize = path.getsize(datPath)
        rowCount = int(datSize / LINE_BYTES_SIZE)
    except:
        datSize = 0
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
            'path': csvPath.replace(FOLDER_CSV_IN, 'csv/'),
            'size': csvSize
        },
        'dat': {
            'path': datPath.replace(FOLDER_DAT_IN, 'dat/'),
            'size': datSize
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
