"""
Initial cleanup file for google maps scraper output
- Delete unnecessary columns
- Delete any results with errors
- Delete any results with no website
- Requires
    python install from web?
    pandas 'pip/conda install pandas'

TODO
 * Delete original data file?
 * output message to terminal of results and new file name/path

"""
# Pandas - data analysis module for python
import sys
import pandas as pd

# Read contents of csv file specified in commandline
filepath = sys.argv[1]
data = pd.read_csv(filepath)

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

# Output cleaned data frame to new file in same directory as original
temp = filepath.find('.csv')
new_filepath = filepath[:temp] + '_Cleaned' + filepath[temp:]
df.to_csv(new_filepath, index=False)

# Outputs message to terminal indicatng successful run
print('Cleaned file exported to: ' + new_filepath)
