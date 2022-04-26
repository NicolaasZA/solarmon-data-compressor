from src.okahandja import lineToBytes, formatName
from src.files import fileToLines, getFileList
import shutil

directory_in = 'input/'
directory_out = 'compressed/normal/'

ext_in = '.csv'
ext_out = '.dat'

count_coverage = 0
count_lines = 0

files_to_append = getFileList(directory_in, ext_in)

for filePath in files_to_append:
    try:
        # READ IN
        content = fileToLines(filePath)
        count_lines += len(content)
        file_coverage = 0

        out_csv_path = formatName(filePath.replace(directory_in, directory_out))
        out_dat_path = out_csv_path.replace(ext_in, ext_out)

        # WRITE OUT
        with open(out_dat_path, 'wb') as target:
            for line in content:
                data = lineToBytes(line)
                if data is not None:
                    target.write(data)
                    file_coverage += 1

        # COPY IN FILE TO OUT FOLDER
        shutil.copyfile(filePath, out_csv_path)

        count_coverage += file_coverage
        print(f'Finished {filePath}, {file_coverage} of {len(content)} lines')
    except Exception as exc:
        print(f'Failed to compress {filePath}', exc)


print(f'done, wrote {count_coverage} of {count_lines} lines')



