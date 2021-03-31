"""
Data Cleaning Script for Eblast results CSV

TODO:
 * documentation
 * debug mode?

"""
# Pandas - data analysis module for python
import sys
import pandas as pd

# Read contents of csv file specified in commandline input
filepath = sys.argv[1]
data = pd.read_csv(filepath)

# Convert CSV data to Data Frame (Pandas object) for easier manipulation
df = pd.DataFrame(data)

print(df.info())

# Check last column of data frame to see if it is log file of email opens
# or a file of email clicks. For the email clicks file we will drop all info
# that will not be used in searching dataframe to add to correct spot.
# informaiton on leads should already be in dataframe from processing email open.

if df.columns[-1] == 'Opened At':
    # Keep only columns:
    # Email address, First name, Last name, Company, Job title, Email status,
    # Phone - mobile, Phone - work, Street address line 1 - Home, City - Home,
    # State/Province - Home, Zip/Postal Code - Home, Website, Industry,
    # Annual Revenue, number of employees, Tags, Opened At
    deletion_list = ['Email permission status', 'Email update source', \
        'Confirmed Opt-Out Date','Confirmed Opt-Out Source', \
        'Confirmed Opt-Out Reason', 'Salutation', \
        'Email Lists', 'Source Name', 'Created At', 'Updated At']

elif df.columns[-1] == 'Clicked At':
    print("click log file found")
    # Keep only columns:
    # Email address, First name, Last name, Tags, Clicked Link Address, Opened At
    deletion_list = ['Company','Job title','Email permission status',\
        'Email update source','Phone - home','Phone - mobile', 'Phone - work',\
        'Street address line 1 - Home', 'City - Home', \
        'State/Province - Home', 'Country - Home', \
        'Zip/Postal Code - Home', 'Website',\
        'Industry', 'Annual Revenue', 'Initial Email Status', 'Company LI',\
        'LinkedIn URL','number of employees','Prospect Location', \
        'Location of Contact', 'Infogroup ID','Gender','Email Lists', \
        'Source Name','Created At','Updated At',]

else:
    print('NOTE: Unfamilier CC file type.')


#drop columns depending on file type
df = df.drop(deletion_list, axis = 1, errors = 'ignore')

# Generate new filepath to store the cleaned file
# [original file name]_Cleaned.csv in same directory as original file path
temp = filepath.find('.csv')
new_filepath = filepath[:temp] + '_Cleaned' + filepath[temp:]

# Output data to new filepath as CSV
df.to_csv(new_filepath, index=False)

# Outputs message and new filepath to terminal
print('Cleaned file exported to: ' + new_filepath)
print(df.info())
