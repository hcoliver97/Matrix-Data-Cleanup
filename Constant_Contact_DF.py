"""
Updates Constant Contact DF CSV using most recent verison of open
and click log CSVs from Constant Contact

input:
    Open Logs - Download from CC, contains email, open timestamp, other lead info.
                Each row is one lead with unique email address.

    Click Logs - Download from CC, contains email, clicked timestamp,
                clicked links. Each row is one click.

NOTE: This does not drop leads who have unsubsribed. Filter as needed later.

1. Creates DF file if none exists in script directory
2. Reads in CSV from directory specified in commandline,
    calls Data_Cleanup script to clean the data.
3. Check and store filetype (Clicks or Opens) in variable.
3. If Open log is read in and DF file is empty, populate DF with
    cleaned open log data.
4. Condense click log data to one row per unique email address.
    'Clicked At' - first click timestamp
    'Clicked Link Address' - URLs separated by ' ,'
5. Insert click log data into row of associated email address
6. Output updated DF to CSV.

TODO:
    - If DF is not empty, add only new values from Open log to DF.
    - Handle reading in newer versions of click log
    - Handle dealing with file and DF names
        Maybe by having client name in a variable to read in and insert etc.

"""

import sys
import pandas as pd
import numpy as np
import os.path
from os import path
import Data_Cleanup

# Client Name - 'First_Last'
#               Who'se CC data are we processing?
#               Used in naming files and reading in files.
client = 'Brandee_Justus'
client_DF_name = client+'_CC_DF.csv'

# Check if CC DataFrame CSV has already been created in script directory.
# TODO: Maybe chance cc_updated to more descriptive name
if path.exists(client_DF_name):
    # If the DF exists, read in CSV data and store as DataFrame object
    cc_updated = pd.read_csv(client_DF_name)
    cc_updated = pd.DataFrame(cc_updated)
else:
    # If DF CSV does not exist, create new DataFrame object
    cc_fields = ['Email address', 'First name', 'Last name','Company',\
    'Job title','Email status','Phone - home','Phone - mobile',\
    'Phone - work','Street address line 1 - Home','City - Home',\
    'State/Province - Home','Zip/Postal Code - Home','Country - Home',\
    'Website','Industry','Annual Revenue','Company LI','LinkedIn URL',\
    'number of employees','Tags','Opened At','Clicked Link Address',\
    'Clicked At']

    cc_updated = pd.DataFrame(columns = cc_fields)

# Read in CC data file specified in commandline and store as DataFrame object
input_filepath = sys.argv[1]
input_data = pd.read_csv(input_filepath)
input_df = pd.DataFrame(input_data)

# Call Data_Cleanup script on read in data
#   The script will determine what file time it has recieved and clean
#   to specificatin of that file type.
input_df = Data_Cleanup.data_cleanup(input_df)

# Check the last column of the DataFrame to determine what file type has been
# read in and store in variable for later use.
if input_df.columns[-1] == 'Opened At':
    # file_type 0 - CC email opens log CSV.
    file_type = 0
elif input_df.columns[-1] == 'Clicked At':
    # file_type 1 - CC click log CSV.
    file_type = 1
else:
    print('NOTE: Unfamilier CC file type.')

# Start processing the input data.
# Email open logs:
if file_type == 0:
    # Check if client DF is empty
    if cc_updated.empty:
        # If empty, add input data to client dataframe as is.
        # 'Click Link Address' and 'Clicked At' columns will remain empty
        # in the client dataframe.
        cc_updated = pd.concat([cc_updated, input_df])
    else:
        # *** TODO ***
        # if dataframe not empty, add unique entries only
        # for "opened at" > top "opened at" in DF, add row to DF
        print("File type: Open log")

# Click logs:
elif file_type == 1:
    # Save only first timestamp for each unique email address
    clicked_at = input_df.groupby('Email address').agg({'Clicked At':'first'}).reset_index()
    # Combine clicked links for each unique email adrress seperated by ', '
    clicked_links = input_df.groupby('Email address').agg({'Clicked Link Address':', '.join}).reset_index()

    # Drop duplicate email addresses from the click log dataframe
    input_df = input_df.drop_duplicates(subset=['Email address'],ignore_index = True)

    # Load timestamp and clicked url CSV into 'Clicked At' and
    # 'Clicked Link Address' into the click log dataframe
    # *** TODO ***
    # Is adding timestamp again redundant when it alreay exists associated
    # with the email address?
    input_df['Clicked At'] = clicked_at['Clicked At']
    input_df['Clicked Link Address'] = clicked_links['Clicked Link Address']

    #*** TODO ***
    # Merge input_df and cc_updated DF so that the 'Clicked At' and
    #   'Clicked Link Address' will be updated at row corresponding to
    #   email address
    # 1. lookup email address in 'Email Address' column
    # 2. Insert 'Clicked At' data at that index df.insert(loc,column,value)
    # 3. Insret 'Clicked Link Address' data at that indexes
    for ind in input_df.index:
        email = input_df['Email address'][ind]
        df_ind = cc_updated['Email address'][cc_updated['Email address'] == email].index.tolist()
        clicked_at_data = input_df['Clicked At'].values[ind]
        clicked_links = input_df['Clicked Link Address'].values[ind]
        cc_updated.loc[df_ind,'Clicked At'] = clicked_at_data
        cc_updated.loc[df_ind,'Clicked Link Address'] = clicked_links

else:
    print('NOTE: Unfamilier CC file type.')


# Ouput the client DataFrame to CSV file for storage.
# Ignore index because we don't want indexing column added new every tiem
# we write to the file.
#print(cc_updated.info())
#print(input_df)
cc_updated.to_csv(client_DF_name, index = False)
