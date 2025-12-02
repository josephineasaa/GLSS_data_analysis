#this script converts the "17_GHA_2017_INCOME" data with the region names rather than the region codes

import pandas as pd

file = "others/2017/g7aggregates/17_GHA_2017_INCOME.dta"
df = pd.read_stata(file)

print(df["region"].unique())

csv = df.to_csv("17_GHA_2017_INCOME")