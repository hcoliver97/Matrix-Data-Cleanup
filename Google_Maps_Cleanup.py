"""
Data Cleaning Script for Google Maps Scraper Output
    input - filepath to CSV file to clean
    output - CSV file containing cleaned data saved to original directory

    This script takes in a CSV file of data collected from Google Maps
    listings and deletes unnecessary columns and deletes rows containing
    errors or lacking necessary fields.

    The data is stored as a new CSV in the directory containing original
    CSV file. A filepath to the new CSV is printed to terminal upon succesdful
    execution.

TODO
 * Delete original data file?
 * Error/edge case handlling:
    - Make it so it can handle if there isnt enough input columns
    - Check if the necessary columns exist?

"""
# Pandas - data analysis module for python
import sys
import pandas as pd

# Read contents of csv file specified in commandline input
filepath = sys.argv[1]
data = pd.read_csv(filepath)

# Convert CSV data to Data Frame (Pandas object) for easier manipulation
df = pd.DataFrame(data)

# Test Drop
df = df.drop(['rating', 'reviewCount',],axis = 1)

# Delete unnecessary columns from Data Frame
# Can be updated to fit client need
# Keeping only columns:
# placeUrl, title, category, address, website, phoneNumber, openingHours,
# isClaimed, latitude, and longitude.

deletion_list = ['subtitle', 'rating', 'reviewCount', \
        'attributes', 'plusCode', 'imgUrl', 'query', 'timestamp',\
        'tuesday','wednesday','thursday','friday','saturday',\
        'sunday','monday']

# Deletes columns if they exist, ignores error otherwise
df = df.drop(deletion_list, axis = 1, errors = 'ignore')

# Keep only results (rows) with no errors (error is null)
# All rows containing erorrs in scraping process are deleted
df = df[df.error.isna()]

# Keep only results (rows) with a website (website is not null)
# Every row will have an associated website now
df = df[df.website.notna()]

# Drop error column since every row is error free now
df = df.drop(['error'], axis = 1)

# Generate new filepath to store the cleaned file
# [original file name]_Cleaned.csv in same directory as original file path
temp = filepath.find('.csv')
new_filepath = filepath[:temp] + '_Cleaned' + filepath[temp:]

# Output data to new filepath as CSV
df.to_csv(new_filepath, index=False)

# Outputs message and new filepath to terminal
print('Cleaned file exported to: ' + new_filepath)
