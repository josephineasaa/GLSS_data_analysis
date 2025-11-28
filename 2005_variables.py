import pandas as pd
import os
from typing import List, Dict
 
def read_csv_file(file_path: str, usecols: List[str]) -> pd.DataFrame:
    try:
        return pd.read_csv(file_path, usecols=usecols)
    except Exception as e:
        raise ValueError(f"Error reading {file_path}: {e}")
 
def merge_files(file_columns: Dict[str, List[str]]) -> pd.DataFrame:
    merged_df = None
    for file, cols in file_columns.items():
        df = read_csv_file(file, ['CLUST', 'NH'] + cols)
        df = df.drop_duplicates(subset=['CLUST', 'NH'])  
 
        if merged_df is None:
            merged_df = df
        else:
            merged_df = pd.merge(merged_df, df, on=['CLUST', 'NH'], how='outer')
 
    return merged_df.fillna(0)
 
def add_region_column(merged_df: pd.DataFrame, sec0_path: str) -> pd.DataFrame:
    try:
        sec0_df = pd.read_csv(sec0_path, usecols=['CLUST', 'REGION'])
        sec0_df['CLUST'] = sec0_df['CLUST'].astype(str).str.replace(r'\.0$', '', regex=True)
        sec0_df = sec0_df.drop_duplicates(subset=['CLUST'])  
 
        merged_df['CLUST'] = merged_df['CLUST'].astype(str).str.replace(r'\.0$', '', regex=True)
        merged_df = merged_df.merge(sec0_df, on='CLUST', how='left')
        merged_df.rename(columns={'REGION': 'region'}, inplace=True)
 
        return merged_df
    except Exception as e:
        raise ValueError(f"Error processing sec0.csv: {e}")
 
def compute_total_income(merged_df: pd.DataFrame) -> pd.DataFrame:
    try:
        merged_df['TOT_HH_INC_NET'] = (
            merged_df['TOTEMP'] + merged_df['AGRI1C'] + merged_df['AGRI2C'] +
            merged_df['NFSEY1'] + merged_df['NFSEY2'] + merged_df['NFSEY3'] +
            merged_df['IMPRT'] + merged_df['REMITINC'] + merged_df['OTHERINC'] -
            merged_df['EXPFOODC'] - merged_df['HOUSEXP'] - merged_df['OTHEXPC'] -
            merged_df['EXPREMIT']
        )
        return merged_df
    except KeyError as e:
        raise ValueError(f"Missing column in computation: {e}")
 
def main():
    file_columns = {
        "2005_aggregates_csv/AGG1.csv": ["TOTEMP"],
        "2005_aggregates_csv/AGG2.csv": ["AGRI1C", "AGRI2C"],
        "2005_aggregates_csv/AGG3.csv": ["NFSEY1", "NFSEY2", "NFSEY3"],
        "2005_aggregates_csv/AGG4.csv": ["IMPRT"],
        "2005_aggregates_csv/AGG5.csv": ["REMITINC"],
        "2005_aggregates_csv/AGG6.csv": ["OTHERINC"],
        "2005_aggregates_csv/AGG7.csv": ["EXPFOODC"],
        "2005_aggregates_csv/AGG8.csv": ["HOUSEXP"],
        "2005_aggregates_csv/AGG9.csv": ["OTHEXPC"],
        "2005_aggregates_csv/AGG12.csv": ["EXPREMIT"]
    }
    sec0_path = "2005_parta_csv/sec0.csv"
    output_file = "GHA_2005_income.csv"
 
    merged_df = merge_files(file_columns)
    merged_df = add_region_column(merged_df, sec0_path)
    merged_df = compute_total_income(merged_df)
    merged_df.to_csv(output_file, index=False)
 
if __name__ == "__main__":
    main()


