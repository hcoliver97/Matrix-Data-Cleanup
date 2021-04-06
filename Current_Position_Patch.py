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

# Function to check org title for

def find_key(title):
    # Position key words
    keys = ['Owner', 'Founder', 'President']
    for key in keys:
        if search(key, title):
            #title found
            return True
        else:
            #title not found, check next title in keys
            continue
    #none of the keys were found in title
    return False

for index in input_df.index:
    name = input_df['last_name'][index]
    for i in [1, 2, 3, 4]:
        if input_df['organization_title_'+str(i)][index] == 'nan':
            # no title exists
            print('NOTE: no further titles to check')
            break
        current_title = input_df['organization_title_'+str(i)][index]
        current_org = input_df['organization_'+str(i)][index]
        if find_key(current_title):
            # Title contains one of key words
            print(name + ': ' + current_title)
            break
        else:
            continue

        # Name didn't contain titles, reset current title to the first org
        print(name + ': title not found')
        current_title = input_df['organization_title_1'][index]
        current_org = input_df['organization_1'][index]

    input_df['current_company_position'][index] = current_title
    input_df['current_company'][index] = current_org

# Output Data to CSV
input_df.to_csv('Brandee_Justus_All_LI_Updated.csv', index = False)
