"""
Sample Script to Convert Company Lead Info CSVs into one big CSV

 - read in csv file to process
 - check row if unique in business_lead_df

 TODO:
    * pass data through cleaning protocol
    * where to check for CSV and where to output it

"""
import sys
import pandas as pd
import numpy as np
import os.path
from os import path
import Data_Cleanup

# Check if business_lead_df CRV has already been created.
# Read CSV to populate DataFrame or create new with given columns
if path.exists('business_lead_df.csv'):
    # Read in CSV to Data frame
    business_lead_df = pd.read_csv('business_lead_df.csv')
    business_lead_df = pd.DataFrame(business_lead_df)
else:
    # Create business lead data frame if CSV file with leads doesn't exist
    bl_fields = ['title','sector', 'website', 'phoneNumber', 'address',\
        'linkedInUrl', 'size', 'revanue', 'contactPerson']

    business_lead_df = pd.DataFrame(columns = bl_fields)

# Read in file specified in commandline
# TODO: right now it only handles cleaned google maps search files
# if first column is placeUrl then its a google maps export file
input_filepath = sys.argv[1]
input_data = pd.read_csv(input_filepath)
input_df = pd.DataFrame(input_data)
# call clean data and pass input_df into it
Data_Cleanup.data_cleanup(input_df)

# Rename + add columns to match format of business lead data frame
# TODO: Make a check for if these columns already exist
input_df.rename(columns = {'category':'sector'}, inplace = True)
input_df['linkedInUrl'] = np.nan
input_df['size'] = np.nan
input_df['revanue'] = np.nan
input_df['contactPerson'] = np.nan

# Add input data to the business lead dataframe
# Data shouls be added to bottom of dataframe while ignoring indexing
# associated with input dataframe. Inner join meaning only columns in
# both data frames will be added
business_lead_df = pd.concat([business_lead_df,input_df], axis = 0, \
    ignore_index = True, join = 'inner')

# Drop any duplicate entries according to pandas own checking algorithm
# --> Not sure if most efficient for our purposes but will do for now
# and reset the indexes so the whole sheet has unique indecies from 0 to (n-1)
business_lead_df.drop_duplicates().reset_index(drop = True)

# Write filled business lead data frame to CSV file
business_lead_df.to_csv('business_lead_df.csv')
