def filesToLines(fileNames: list):
    lines = []
    for filePath in fileNames:
        with open(filePath, 'r') as source:
            lines = lines + source.readlines()
    return lines