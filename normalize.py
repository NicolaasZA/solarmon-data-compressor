from src.okahandja import getDateFromBytes, getTimeValueFromBytes
from src.files import getFileList

dir_in = 'compressed/normal/'
dir_out = 'compressed/'

ext_in = '.dat'

count_coverage = 0
count_lines = 0

# ['compressed/dat/okh_2022_04_14.dat']
files_to_process = getFileList(dir_in, ext_in)

# Import
data: bytes = []
for file_path in files_to_process:
    with open(file_path, 'rb') as input:
        data += input.read()

import_size = round((len(data) / 1000.0) / 1000.0, 2)
print(f'imported {import_size} MB from {len(files_to_process)} files')

# Normalize
normalized = {}

start = 0
while start < len(data):
    line = data[start:start+24]
    _key = getDateFromBytes(line)

    if _key in normalized:
        normalized[_key].append(line)
    else:
        normalized[_key] = [line]
    start += 24

# Write
for dt in normalized:
    out_lines = sorted(normalized[dt], key=lambda d: getTimeValueFromBytes(d))

    out_date = f'{dt}'.replace('-', '_')
    out_path = f'{dir_out}okh_{out_date}.dat'

    with open(out_path, 'wb') as out:
        for line in out_lines:
            out.write(bytearray(line))
        print(f'Normalized {dt} to {out_path}')

print('done')
