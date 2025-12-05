**GLSS_convert_sav.py — Script overview**

This file documents the `GLSS_convert_sav.py` script. The script searches several repository folders for SPSS (`.sav`) and Stata (`.dta`) files, converts each to CSV, and writes them into parallel folders with the `_csv` suffix.

**Purpose**
- Convert legacy survey data files (`.sav`, `.dta`) into CSV for easier downstream processing with Python or other tools.

**What the script does**
- Iterates a hard-coded list of `folder_paths` (relative to the repository root).
- For each existing folder:
  - Creates a sibling folder named `<folder>_csv` (if it does not already exist).
  - Lists files in the source folder and filters for `.sav` and `.dta` extensions (case-insensitive).
  - For each file found, attempts to read it using `pandas.read_spss` (for `.sav`) or `pandas.read_stata` (for `.dta`).
  - If the file contains data, writes it to CSV in the `_csv` folder using `DataFrame.to_csv(..., index=False)`.
  - Prints progress and any errors encountered; skips missing folders or files with no readable data.

**Folders scanned (current script)**
- `2005 with csvs/aggregates`
- `2005 with csvs/parta`
- `2005 with csvs/section10`
- `1991-1992/aggreg`
- `1991-1992/Prices`
- `1998/aggreg`
- `1998/Prices`
- `2012-2013/AGGREGATES`
- `2012-2013/PARTA`
- `2012-2013/PRICES`
- `2017/g7aggregates`
- `2017/g7PartA`
- `2017/g7price`

**Outputs**
- For a source folder `X`, the script creates (or re-uses) `X_csv` and writes converted CSV files there. Filenames preserve the original base name with a `.csv` extension.

**Requirements**
- Python 3.7+.
- `pandas` (tested on pandas 1.x+). Install with:

```powershell
pip install pandas pyreadstat
```

Note: `pandas.read_spss` and `read_stata` rely on the `pyreadstat` backend for many formats; installing `pyreadstat` ensures better compatibility when reading `.sav` and `.dta` files.

**Usage**
- From the repository root run:

```powershell
python GLSS_convert_sav.py
```

**Behavior & logging**
- The script prints human-readable messages to stdout for:
  - Skipped folders that do not exist
  - Files being processed
  - Success messages for converted files
  - Errors encountered while reading or writing files
- It does not currently return non-zero exit codes for failures; all exceptions are caught and printed so the script attempts to continue processing other files.

**Notes & recommended improvements**
- The `folder_paths` list is hard-coded. Consider accepting a base directory or adding a CLI (`argparse`) to supply folders or recursive scanning.
- Improve error handling: return non-zero exit code on critical failures (useful for CI), or collect a summary report at the end.
- Use logging (`logging` module) instead of `print` for better verbosity control and optional log files.
- Optionally skip files already converted (compare timestamps or check if CSV exists) to make the script idempotent and faster on repeated runs.

If you want, I can:
- Add a CLI to pass a list of folders or enable recursive scanning,
- Add environment-aware behavior (e.g., set input/output base paths), or
- Replace prints with structured logging and a summary at the end.
