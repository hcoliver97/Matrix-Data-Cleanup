"""
Initial cleanup file for google maps scraper output
- Delete unnecessary columns
- Delete any results with errors
- Delete any results with no website
- Requires
    python install from web?
    pandas 'pip/conda install pandas'

TODO
 * take in file to clean as input
 * generate new csv file of cleaned data
    - delete original one?
 * output message to terminal of results and new file name/path

"""
# Pandas - data analysis module for python
import pandas as pd

# Read contents of csv
# TODO - convert to use file path of file from input
data = pd.read_csv('~/Documents/Matrix/GoogleSearchResults.csv')

# Convert CSV file content to Data Frame for easier manipulation
df = pd.DataFrame(data)

# Delete unnecessary columns from Data Frame
# Keeping only columns:
# placeUrl, title, category, address, website, phoneNumber, openingHours,
# isClaimed, latitude, and longitude.
df = df.drop(['subtitle', 'rating', 'reviewCount', \
        'attributes', 'plusCode', 'imgUrl', 'query', 'timestamp',\
        'tuesday','wednesday','thursday','friday','saturday',\
        'sunday','monday'], axis = 1)

# Keep only results (rows) with no errors (error is null)
df = df[df.error.isna()]

# Keep only results (rows) with a website (website is not null)
df = df[df.website.notna()]

# Drop error column since every row is error free now
df = df.drop(['error'], axis = 1)

# Print information about remaining data frame
print(df.info())
