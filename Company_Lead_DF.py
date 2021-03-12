"""
Business Lead Data Frame script
    - Takes in CSV files containing human lead info and compiles into dataframe
    - Currenty supports:
        Google Maps Export CSV (PhantomBuster)
        SN Search Exort CSV (PhantomBuster)
    - Cleans data using Data_Cleanup script

TODO:
    * Handling export of cleaned data to CSV?
    * Support more file filetypes
    * Integration with business lead dataframe
    * Add debug mode?

"""
import sys
import pandas as pd
import numpy as np
import os.path
from os import path

# Check if business_lead_df CSV has already been created.
# Read CSV intp dataframe or create new dataframe if file doesn't exists
if path.exists('business_lead_df.csv'):
    # Read CSV into Data frame
    business_lead_df = pd.read_csv('business_lead_df.csv')
    business_lead_df = pd.DataFrame(business_lead_df)
else:
    # Create dataframe with given columns
    bl_fields = ['title','sector', 'website', 'phoneNumber', 'address',\
        'linkedInUrl', 'size', 'revanue', 'contactPerson']
    business_lead_df = pd.DataFrame(columns = bl_fields)

# Read in file specified in commandline
# This is the new data to be cleaned and added to dataframe
input_filepath = sys.argv[1]
input_data = pd.read_csv(input_filepath)
input_df = pd.DataFrame(input_data)
# Clean data via call to Data_Cleanup script
input_df = Data_Cleanup.data_cleanup(input_df)

# Rename + add columns to match format of business lead data frame
# TODO: Checking if columns exist
input_df.rename(columns = {'category':'sector'}, inplace = True)
# These columns are for data to be added from other sources so emoty for now
input_df['linkedInUrl'] = np.nan
input_df['size'] = np.nan
input_df['revanue'] = np.nan
input_df['contactPerson'] = np.nan

# Add new data to the bottom of the business lead dataframe
# Old indecies associated with input_data are ignored and inner join
# preserving only columns the two dataframes have in common are added
business_lead_df = pd.concat([business_lead_df,input_df], axis = 0, \
    ignore_index = True, join = 'inner')

# Drop any duplicate entries according to pandas own checking algorithm
# TODO: Not sure if most efficient for our purposes
# Reset the indexes so the whole sheet has unique indecies from 0 to (n-1)
business_lead_df.drop_duplicates().reset_index(drop = True)

# Write updated business lead data frame to CSV file
business_lead_df.to_csv('business_lead_df.csv')
