from src.okahandja import lineToBytes
from src.files import fileToLines

files_to_append = [
    'input/okahandja_2021_10_1.csv',
    'input/okahandja_2021_10_2.csv',
    'input/okahandja_2021_10_3.csv',
    'input/okahandja_2021_10_4.csv',
    'input/okahandja_2021_10_5.csv',
    'input/okahandja_2021_10_6.csv',
    'input/okahandja_2021_10_7.csv',
    'input/okahandja_2021_10_8.csv',
    'input/okahandja_2021_10_9.csv',
    'input/okahandja_2021_10_10.csv',
    'input/okahandja_2021_10_11.csv',
    'input/okahandja_2021_10_12.csv',
    'input/okahandja_2021_10_13.csv',
    'input/okahandja_2021_10_14.csv',
    'input/okahandja_2021_10_15.csv',
    'input/okahandja_2021_10_16.csv',
    'input/okahandja_2021_10_17.csv',
    'input/okahandja_2021_10_18.csv',
    'input/okahandja_2021_10_19.csv',
    'input/okahandja_2021_10_20.csv',
    'input/okahandja_2021_10_21.csv',
    'input/okahandja_2021_10_22.csv',
    'input/okahandja_2021_10_23.csv',
    'input/okahandja_2021_10_24.csv',
    'input/okahandja_2021_10_25.csv',
    'input/okahandja_2021_10_26.csv',
    'input/okahandja_2021_10_27.csv',
    'input/okahandja_2021_10_28.csv',
    'input/okahandja_2021_10_29.csv',
    'input/okahandja_2021_10_30.csv',
    'input/okahandja_2021_10_31.csv'
]

directory_in = 'input/'
directory_out = 'compressed/'

count_coverage = 0
count_lines = 0

for filePath in files_to_append:
    # READ IN
    content = fileToLines(filePath)
    count_lines += len(content)

    # WRITE OUT
    with open(filePath.replace(directory_in, directory_out), 'wb') as target:
        for line in content:
            data = lineToBytes(line)
            if data is not None:
                target.write(data)
                count_coverage += 1


print(f'done, wrote {count_coverage} of {len(count_lines)} lines')



