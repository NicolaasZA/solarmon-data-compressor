import glob
import json
import os


def filesToLines(fileNames: list):
    lines = []
    for filePath in fileNames:
        with open(filePath, 'r') as source:
            lines = lines + source.readlines()
    return lines


def fileToLines(fileName: str) -> list[str]:
    lines = []
    with open(fileName, 'r') as source:
        lines = lines + source.readlines()
    return lines


def fileToBytes(filePath: str) -> bytes:
    data: bytes = []
    with open(filePath, 'rb') as input:
        data += input.read()
    return data


def fileAsJSON(filePath: str):
    text = fileToLines(filePath)
    return json.loads("".join(text))


def getFileList(directoryName: str, targetExt: str):
    if not directoryName.endswith('/'):
        directoryName = directoryName + '/'
    files = []
    root = glob.glob(f'{directoryName}*')
    for target in root:
        if target.endswith(targetExt) and os.path.isfile(target):
            files.append(target)
        elif os.path.isdir(target):
            # Recursively loop in
            files = files + getFileList(target, targetExt)
    return files
