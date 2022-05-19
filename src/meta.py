import glob
from src.files import fileAsJSON


def findIndex(meta_arr: list, date: str):
    idx = 0
    for i in meta_arr:
        if i['date'] == date:
            return idx
        idx += 1
    return -1


def metaPaths(in_meta: list, folder_in_path: str):
    res: list[str] = []

    for mf in in_meta:
        dt = mf['date'].replace('-', '_')
        path = f'{folder_in_path}okh_{dt}.dat'
        res.append(path)

    return res


def filesToProcessFromPaths(folder_in_path: str, meta_config_path: str):
    """Returns three lists: to_process_paths, in_directory_paths, in_meta_files"""
    in_directory_paths = glob.glob(folder_in_path + '*.dat')

    try:
        to_process_paths: list[str] = []
        config = fileAsJSON(meta_config_path)
        in_meta_paths = metaPaths(config['files'], folder_in_path)

        for df in in_directory_paths:
            if df not in in_meta_paths:
                to_process_paths.append(df)
        return to_process_paths, in_directory_paths, config['files']
    except:
        # If there is not existing meta.json file, process everything
        return in_directory_paths, in_directory_paths, []
