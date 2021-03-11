"""
Sample Script to Convert Company Lead Info CSVs into one big CSV

 - read in csv file to process
 - check row if unique in business_lead_df

 TODO:
    * pass data through cleaning protocol


"""
import sys
import pandas as pd
import os.path
from os import path
#import Data_Cleanup


if path.exists('business_lead_df.csv'):
    business_lead_df = pd.read_csv('business_lead_df.csv')
    business_lead_df - pd.DataFrame(business_lead_df)
else:
    # Create business lead data frame --> we want to keep adding to existing csv
    # so this needs to be if csv file for existing business lead df isnt existing
    bl_fields = ['title','sector', 'website', 'phoneNumber', 'address',\
        'linkedInUrl', 'size', 'revanue', 'contactPerson']

    business_lead_df = pd.DataFrame(columns = bl_fields)

# Read in iput files, make sure to check if cleaned or run cleaning module on it
input_filepath = sys.argv[1]

input_data = pd.read_csv(input_filepath)
input_df = pd.DataFrame(input_data)
input_df.rename(columns = {'category':'sector'}, inplace = True)
# clean data

# Add cleaned data entries to business_lead_df
business_lead_df = pd.concat([business_lead_df,input_df], axis = 0, \
    ignore_index = True, join = 'inner')
print(business_lead_df.info())

#drop duplicate entries --> check if it works proeprly
business_lead_df.drop_duplicates().reset_index(drop = True)

# Publish processed dataframe to CSV file
business_lead_df.to_csv('business_lead_df.csv')
