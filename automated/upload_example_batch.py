# python -m pip install requests

import requests
import glob
import os

def getFileList(directoryName: str, targetExt: str) -> list[str]:
    if not directoryName.endswith('/'):
        directoryName = directoryName + '/'
    files = []
    root = glob.glob(f'{directoryName}*')
    for target in root:
        if target.endswith(targetExt) and os.path.isfile(target):
            files.append(target)
        elif os.path.isdir(target):
            files = files + getFileList(target, targetExt)
    return files


def uploadFile(path: str, dateString: str) -> str:
    files = {'fileToUpload': open(path, 'rb')}
    data = {'date': dateString}

    r = requests.post('https://data.klausius.co.za/okahandja/endpoint.php', files=files, data=data)
    return r.text


ext = '.csv'

filesToUpload = sorted(getFileList('send', ext))

for path in filesToUpload:
    # Get date
    fileName = path.split('/')[-1]
    fileDate = fileName.removeprefix('okh_').removesuffix(ext).replace('_', '-')

    # Upload
    result = uploadFile(path, fileDate)
    print(fileName + ' -> ' + result)

    # Remove
    if result == '200':
        os.remove(path)
