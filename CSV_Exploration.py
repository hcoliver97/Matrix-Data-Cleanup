# Pandas - data analysis module for python
import sys
import pandas as pd
import numpy as np

# Read contents of csv file specified in commandline input
filepath = sys.argv[1]
data = pd.read_csv(filepath)

# Convert CSV data to Data Frame (Pandas object) for easier manipulation
df = pd.DataFrame(data)

print("Imported DataFrame:")
print(df.info())

print("First 10 rows:")
print(df.head(10))
