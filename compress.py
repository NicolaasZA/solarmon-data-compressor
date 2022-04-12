from src.okahandja import lineToBytes
from src.files import filesToLines

files_to_append = [
    'input/okahandja_2022_4_5.csv',
    # 'input/okahandja_2022_4_6.csv',
    # 'input/okahandja_2022_4_7.csv',
    # 'input/okahandja_2022_4_8.csv',
    # 'input/okahandja_2022_4_9.csv'
]

file_out = 'output/okahandja_2022_04.txt'

# READ IN
lines = filesToLines(files_to_append)

# WRITE OUT
coverage = 0
with open(file_out, 'wb') as target:
    for line in lines:
        data = lineToBytes(line)
        if data is not None:
            target.write(data)
            coverage += 1

print(f'done, wrote {coverage} of {len(lines)} lines')
