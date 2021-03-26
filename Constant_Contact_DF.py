"""
Updates Constant Contact output CSV using most recent verison

TODO:
    - It will create and populate initial John_Grillos_CC_Updated.csv fine
        but checking if email values match between updated file and input file
        reults in errors
    - handle new openings, status Updates
    - handle logging clickthroughs


"""

import sys
import pandas as pd
import numpy as np
import os.path
from os import path
import Data_Cleanup

# Check if human_lead_df CSV has already been created.
# Read CSV to populate human_lead_df or create new with given columns
if path.exists('John_Grillos_CC_Updated.csv'):
    # Read in CSV data
    cc_updated = pd.read_csv('John_Grillos_CC_Updated.csv')
    cc_updated = pd.DataFrame(cc_updated)
else:
    # Create human lead data frame if CSV file with leads doesn't exist
    # TODO: Error handling
    cc_fields = ['Email address', 'First name', 'Last name', 'Company', \
    'Job title', 'Email status', 'Phone - mobile', 'Phone - work', \
    'Street address line 1 - Home', 'City - Home',
     'State/Province - Home', 'Zip/Postal Code - Home', 'Website', \
     'Industry', 'Annual Revenue', 'number of employees', 'Tags', 'Opened At']

    cc_updated = pd.DataFrame(columns = cc_fields)



# Read in newer CC info CSV specified in input
input_filepath = sys.argv[1]
input_data = pd.read_csv(input_filepath)
input_df = pd.DataFrame(input_data)

# Clean data by calling Data_Cleanup script
input_df = Data_Cleanup.data_cleanup(input_df)

# Handling new opens
#Check the top value of last version of cc update file.
# If it is the same as the top value of newest CC CSV,
# this means no new opens were made.
new_leads = 0

for lead in input_df['Email address']:
    if cc_updated.empty:
        new_leads = len(input_df)
        break

    if str(cc_updated[lead]['Email address']) == str(input_df[lead]['Email address']):
        #found last updated lead
        break
    else:
        # this lead hasn't been added to updated csv yet
        new_leads = new_leads + 1

# when for loop finishes we should know how many rows of new leads we have
# to add to the updated DF. if there are any to add, concat.
if new_leads > 0:
    cc_updated = pd.concat([input_df.head(new_leads), cc_updated], ignore_index = True)
    # this will add input_df new rows to top of updated cc database
    # now both databases shoud have same rows and columns
    print(cc_updated.info())

# Handling status change
# for each row in updated dataframe, compare email status with corresponding
# row on new csv data. if different, updat the dataframe to match the new data.
"""
for lead in cc_updated['Email address']:
    # check if email status matches for each lead
    if cc_updated['Email status'][lead] == input_df['Email status'][lead]:
        #if they match, no need to update. move to next row.
        continue
    else:
        # if they don't match, set new status to match input csv
        cc_updated['Email status'][lead] == input_df['Email status'][lead]
"""
# at end of for loop all email statuses should be updated

# Write final updated CC data frame to CSV file
cc_updated.to_csv('John_Grillos_CC_Updated.csv')
