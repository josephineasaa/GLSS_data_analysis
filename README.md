**2005_variables.py - README**

- **Purpose**: : This repository-level README documents the `2005_variables.py` script. The script merges a set of 2005 aggregate CSV files, attaches region information from `sec0.csv`, computes household total net income (`TOT_HH_INC_NET`), and writes `GHA_2005_income.csv`.

- **Location**: : The main script is `2005_variables.py` at the repository root. The script expects input CSVs in the following relative folders (from repo root):
  - `2005_aggregates_csv/` (files like `AGG1.csv`, `AGG2.csv`, ..., used to collect columns)
  - `2005_parta_csv/sec0.csv` (provides `CLUST` -> `REGION` mapping)

- **Dependencies**: :
  - Python 3.8+ (recommended)
  - `pandas` (tested with pandas 1.x)

- **What the script does**: :
  1. Reads a predefined set of aggregate CSVs and specific columns (e.g., `TOTEMP`, `AGRI1C`, `NFSEY1`, ...). See the `file_columns` mapping inside `2005_variables.py`.
  2. Merges them on `CLUST` and `NH` (household identifiers), dropping duplicate cluster/household pairs per file.
  3. Loads `sec0.csv` to add a `region` column (from `REGION`) and aligns `CLUST` formatting (removing trailing `.0`).
  4. Computes `TOT_HH_INC_NET` as the sum of income sources minus selected expenditures.
  5. Writes the resulting dataset to `GHA_2005_income.csv` in the repo root.

- **Important file & column expectations**: :
  - Each CSV must include `CLUST` and `NH` columns.
  - `sec0.csv` must include `CLUST` and `REGION`.
  - Column names referenced in `2005_variables.py` must exist in the specified aggregate CSVs.

- **Running the script (PowerShell / pwsh)**: :

```powershell
# from repository root
python .\2005_variables.py
```

- **Output**: :
  - `GHA_2005_income.csv` (written to repository root). The CSV contains merged variables plus `region` and computed `TOT_HH_INC_NET`.

- **Error handling notes**: :
  - The script raises informative `ValueError`-style messages when CSV reads fail or when expected columns are missing in computations. If you see a missing-column error, check the `file_columns` mapping and the corresponding CSVs for that column name.

- **If you only want to push the script today**: :
  - I suggest creating a short, focused branch name such as `push/2005-variables-only` (see recommended commands below). Commit only `2005_variables.py` if you truly want to push only the script and not other repo changes.

- **Suggested branch and commit**: :
  - Branch name: `push/2005-variables-only` (or `feature/2005-variables-readme` if you prefer to include the README on the same branch).
  - Commit message: `Add 2005_variables.py (merge aggregates, compute TOT_HH_INC_NET)`

- **Git commands (PowerShell)**: :

```powershell
# create branch and commit only the script
git checkout -b push/2005-variables-only
git add 2005_variables.py
git commit -m "Add 2005_variables.py (merge aggregates, compute TOT_HH_INC_NET)"
git push -u origin push/2005-variables-only
```

- **Optional (include README on the same branch)**: :

```powershell
# if you want README included on the same branch
git checkout -b feature/2005-variables-readme
git add 2005_variables.py README.md
git commit -m "Add 2005_variables.py and README for 2005 income processing"
git push -u origin feature/2005-variables-readme
```

- **Notes / next steps**: :
  - Verify that all input CSV files exist at the expected relative paths before running.
  - If you want, I can create a small pre-run check in `2005_variables.py` to assert all files exist and list missing files before attempting to read them.

---

If you'd like, I can: create the `README.md` file (I can add it now), produce the exact branch name you prefer, or add a tiny pre-flight check to the script to validate input CSV presence. Which would you like next?