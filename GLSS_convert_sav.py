import os
import pandas as pd

folder_paths = [
    "2005 with csvs/aggregates", "2005 with csvs/parta", "2005 with csvs/section10",
    "1991-1992/aggreg", "1991-1992/Prices", "1998/aggreg", "1998/Prices",
    "2012-2013/AGGREGATES", "2012-2013/PARTA", "2012-2013/PRICES",
    "2017/g7aggregates", "2017/g7PartA", "2017/g7price"
]

for folder in folder_paths:
    if not os.path.exists(folder):
        print(f"Skipping: Folder does not exist - {folder}")
        continue

    csv_folder = f"{folder}_csv"
    os.makedirs(csv_folder, exist_ok=True)

    all_files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    valid_extensions = ["sav", "dta", "SAV", "DTA"]

    data_files = [f for f in all_files if f.split('.')[-1].lower() in valid_extensions]

    if not data_files:
        print(f"No .sav or .dta files found in {folder}")
        continue

    for file in data_files:
        file_path = os.path.join(folder, file)
        file_ext = file.split('.')[-1].lower()
        data = None

        print(f"Processing: {file_path}")

        try:
            if file_ext == "sav":
                print(f"Trying pandas read_spss for {file_path}")
                data = pd.read_spss(file_path)
            elif file_ext == "dta":
                print(f"Trying pandas read_stata for {file_path}")
                data = pd.read_stata(file_path)

            if data is not None and not data.empty:
                csv_file = os.path.join(csv_folder, f"{os.path.splitext(file)[0]}.csv")
                data.to_csv(csv_file, index=False)
                print(f"Successfully converted: {file_path} -> {csv_file}")
            else:
                print(f"Skipping: No data found in {file_path}")
        except Exception as e:
            print(f"Failed to process {file_path}: {e}")

print("All files processed.")
