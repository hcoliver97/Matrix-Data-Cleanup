'''
Update Current Position with Relevant Job Title

- Fill in fields indicated by *** UPDATE *** as they are client specific info


TODO:
 - documentation
 - checking if it is a current position
 - making this a modular Function

'''

import sys
import pandas as pd
import numpy as np
import os.path
from os import path
from re import search
import Data_Cleanup

# ***UPDATE***
# Client Name - First_Last
client = 'Brandee_Justus'

# Read in CC data file specified in commandline and store as DataFrame object
input_filepath = sys.argv[1]
input_data = pd.read_csv(input_filepath)
input_df = pd.DataFrame(input_data)

# Function to check job title string for keywords
def find_key(title):
    # *** UPDATE ***
    # Position key words - different for each client
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
# TODO: Call Cleanup Script to do this
# Keep only columns:
#
deletion_list = ['id', 'public_id','hash_id', 'member_id', 'sn_member_id',\
    'sn_hash_id', 'r_member_id', 't_hash_id', 'lh_id', 'full_name', \
    'original_first_name', 'original_last_name', 'custom_first_name', \
    'custom_last_name', 'avatar', 'summary', 'address', 'birthday',\
    'badges_premium', 'badges_influencer', 'badges_job_seeker', \
    'badges_open_link', 'current_company_custom', \
    'current_company_custom_position', 'organization_id_1', \
    'organization_description_1', 'organization_domain_1', \
    'organization_id_2', 'organization_description_2', 'organization_domain_2',\
    'organization_id_3', 'organization_description_3', 'organization_domain_3',\
    'organization_id_4', 'organization_description_4', 'organization_domain_4',\
    'languages', 'twitters', 'phone_type_1', 'phone_2', 'phone_type_2', \
    'mutual_first_fullname', 'mutual_second_fullname', 'original_mutual_first_fullname',\
    'original_mutual_second_fullname', 'custom_mutual_first_fullname',\
    'custom_mutual_second_fullname','followers','member_distance',\
    'network_info_connection_count', 'network_info_following', 'third_party_email_1',\
    'third_party_email_source_1', 'third_party_email_is_valid_1', 'third_party_email_2',\
    'third_party_email_source_2', 'third_party_email_source_3', \
    'third_party_email_is_valid_2', 'third_party_email_3','third_party_email_is_valid_3' ]

# Deletes columns specified in list if they exist, ignores error otherwise
input_df = input_df.drop(deletion_list, axis = 1, errors = 'ignore')
# TODO: generaliza file output
input_df.to_csv('John_Grillos_All_LI_Leads.csv', index = False)
