from src.okahandja import bytesToLine

FILE_TO_READ = 'output/okahandja_2022_4_5.txt'
FILE_TO_WRITE = 'decompressed/okahandja_2022_4_5.csv'

raw = None
with open(FILE_TO_READ, 'rb') as input:
    raw = input.read()

data = []
for i in range(0, len(raw) + 1, 24):
    data.append(raw[i:i+24])
    i += 24

lines = []
coverage = 0
for entry in data:
    converted = bytesToLine(entry)
    if converted is not None:
        coverage += 1
        lines.append(converted)

with open(FILE_TO_WRITE, 'w') as out:
    out.writelines(lines)

print(f'done, wrote {coverage} of {len(data)} line(s) to {FILE_TO_WRITE}')
