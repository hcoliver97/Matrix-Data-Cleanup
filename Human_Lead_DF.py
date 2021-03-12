"""
Humman Lead Data Frame script
    - Takes in CSV files containing human lead info and compiles into dataframe
    - Currenty supports:
        Google Maps Export CSV (PhantomBuster)
        SN Search Exort CSV (PhantomBuster)
    - Cleans data using Data_Cleanup script

TODO:
    * Handling export of cleaned data to CSV?
    * Support more file filetypes
    * Integration with business lead dataframe
    *

"""

import sys
import pandas as pd
import numpy as np
import os.path
from os import path
import Data_Cleanup

# Check if human_lead_df CSV has already been created.
# Read CSV to populate human_lead_df or create new with given columns
if path.exists('human_lead_df.csv'):
    # Read in CSV data
    human_lead_df = pd.read_csv('human_lead_df.csv')
    human_lead_df = pd.DataFrame(human_lead_df)
else:
    # Create human lead data frame if CSV file with leads doesn't exist
    # TODO: Error handling
    hl_fields = ['firstName', 'lastName', 'companyName', 'jobTitle', \
        'phoneNumber', 'email', 'location', 'linkedInUrl', 'summary']

    human_lead_df = pd.DataFrame(columns = hl_fields)

# Read in file specified in commandline
# Assign that data to a dataframe for easy access/manipulation
input_filepath = sys.argv[1]
input_data = pd.read_csv(input_filepath)
input_df = pd.DataFrame(input_data)

# Clean data by callin Data_Cleanup script
input_df = Data_Cleanup.data_cleanup(input_df)

# Rename/add columns to match format of human lead data frame
# TODO: This is an ugly way of doing this.
input_df.rename(columns = {'title':'jobTitle'}, inplace = True)
input_df.rename(columns = {'profileUrl':'linkedInUrl'}, inplace = True)

# Add input data to bottom of human_lead_df
# Old input_df index column will be ignored, and inner join is perfoemed
# retaining only columns human_lead_df and input_df have in common.
human_lead_df = pd.concat([human_lead_df, input_df], axis = 0, \
    ignore_index = True, join = 'inner')

# Drop any duplicate entries according to pandas own checking algorithm
# TODO: Not sure if most efficient for our purposes
# Reset the indexes so the whole sheet has unique indecies from 0 to (n-1)
human_lead_df.drop_duplicates().reset_index(drop = True)

# Write final human lead data frame to CSV file
human_lead_df.to_csv('human_lead_df.csv')
