'''
Update Current Position with Relevant Job Title

TODO:
 - file Output
 - documentation
 - checking if it is a current position

'''

import sys
import pandas as pd
import numpy as np
import os.path
from os import path
from re import search
import Data_Cleanup

# Read in CC data file specified in commandline and store as DataFrame object
input_filepath = sys.argv[1]
input_data = pd.read_csv(input_filepath)
input_df = pd.DataFrame(input_data)

# Function to check job title string for keywords
def find_key(title):
    # Position key words:
    keys = ['Owner', 'Founder', 'President']
    # Loop through keywords
    for key in keys:
        # Check if keyword is contained in title
        if search(key, title):
            # Keyword found in title
            return True
        else:
            # Keyword not found, check next key
            continue
    # None of the keys were found in the title
    return False

# For each lead in input data
for index in input_df.index:
    # There are up to 4 organizations + positions
    for i in [1, 2, 3, 4]:
        # Check if title is empty (only applicable for org 2 - 4)
        if input_df['organization_title_'+str(i)][index] == 'nan':
            # No title exists to check, move to next row
            break
        # Update current title and organization to that of current org i
        current_title = input_df['organization_title_'+str(i)][index]
        current_org = input_df['organization_'+str(i)][index]
        # Call find_key method to check if title contains key words.
        if find_key(current_title):
            # Returns true if title contains one of key words.
            # Current title, org are the ones we want.
            break
        else:
            # Returns false, title does not contain any of key words.
            # TODO: Error handling?
            continue

        # Name didn't contain titles, reset current title to the first org
        # TODO: Error handling?
        current_title = input_df['organization_title_1'][index]
        current_org = input_df['organization_1'][index]

    # Update current company and position with the company title and org found
    input_df['current_company_position'][index] = current_title
    input_df['current_company'][index] = current_org

# Output Data to CSV file
# TODO: generaliza file output 
input_df.to_csv('Brandee_Justus_All_LI_Updated.csv', index = False)
