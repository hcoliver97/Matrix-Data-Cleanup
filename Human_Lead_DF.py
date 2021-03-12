"""
Sample Script to Convert People Lead Info CSVs into one big CSV

"""

import sys
import pandas as pd
import numpy as np
import os.path
from os import path
import Data_Cleanup

# Check if business_lead_df CRV has already been created.
# Read CSV to populate DataFrame or create new with given columns
if path.exists('human_lead_df.csv'):
    # Read in CSV to Data frame
    human_lead_df = pd.read_csv('human_lead_df.csv')
    human_lead_df = pd.DataFrame(human_lead_df)
else:
    # Create business lead data frame if CSV file with leads doesn't exist
    hl_fields = ['firstName', 'lastName', 'companyName', 'jobTitle', \
        'phoneNumber', 'email', 'location', 'linkedInUrl', 'summary']

    human_lead_df = pd.DataFrame(columns = hl_fields)

# Read in file specified in commandline
# TODO: right now it only handles cleaned google maps search files
# if first column is placeUrl then its a google maps export file
input_filepath = sys.argv[1]
input_data = pd.read_csv(input_filepath)
input_df = pd.DataFrame(input_data)

# call clean data and pass input_df into it
input_df = Data_Cleanup.data_cleanup(input_df)

# Rename + add columns to match format of business lead data frame
# TODO: Make a check for if these columns already exist
input_df.rename(columns = {'title':'jobTitle'}, inplace = True)
input_df.rename(columns = {'profileUrl':'linkedInUrl'}, inplace = True)


# Add input data to the business lead dataframe
# Data shouls be added to bottom of dataframe while ignoring indexing
# associated with input dataframe. Inner join meaning only columns in
# both data frames will be added
human_lead_df = pd.concat([human_lead_df, input_df], axis = 0, \
    ignore_index = True, join = 'inner')

# Drop any duplicate entries according to pandas own checking algorithm
# --> Not sure if most efficient for our purposes but will do for now
# and reset the indexes so the whole sheet has unique indecies from 0 to (n-1)
human_lead_df.drop_duplicates().reset_index(drop = True)

# Write filled business lead data frame to CSV file
human_lead_df.to_csv('human_lead_df.csv')
