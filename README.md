# solarmon-data-compressor

Compresses CSV data into the smallest compatible binary format.

Each project has its own format documentation.

- [Okahandja Solar Project](OKAHANDJA.md)

## Scripts

Python 3 is required to run the scripts.


- `compress.py`

  - Takes all .csv files in the _input/_ folder (including all subfolders)
  - Converts it to binary and dumps out a .dat version inside _compressed/_
  - Also makes a similarly named copy of the input .csv file in _compressed/_

- `stats.py`

  - Grabs a list of all .csv files in _compressed/csv/_
  - Grabs a list of all .dat files in _compressed/dat/_
  - Generate a list of dates, sizes, urls and record counts for these files
  - Writes this data to _compressed/stats.json_

- `normalize.py`
  - The measuring device(s) write to storage at specified intervals. Every day this interval overlaps into the next day around midnight. This means each day's files has a few records of the previous day in it. This script migrates them back to their proper file.
  - Imports all records from all the .dat files in _compressed/dat/_
  - Groups them by date.
  - Writes them back into their proper files.
