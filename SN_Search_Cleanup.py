"""
Data Cleaning Script for LinkedIn Profile Scraper

TODO:
 * Individual Data Cleanup
    - Last names with extra title letters
 * documentation
 * debug mode?

"""
# Pandas - data analysis module for python
import sys
import pandas as pd

if __name__ == '__main__':
    clean()

def clean(df):

    # Keep only
    #   profileUrl, firstName, lastName, companyName, title, companyId, summary,
    #   location duration pastRole pastCompany

    deletion_list = ['name', 'companyUrl', 'pastCompanyUrl', \
        'connectionDegree','profileImageUrl', 'sharedConnectionsCount', 'vmid', \
        'isPremium', 'query', 'timestamp']

    # Deletes columns specified in list if they exist, ignores error otherwise
    df = df.drop(deletion_list, axis = 1, errors = 'ignore')

    # Generate new filepath to store the cleaned file
    # [original file name]_Cleaned.csv in same directory as original file path
    temp = filepath.find('.csv')
    new_filepath = filepath[:temp] + '_Cleaned' + filepath[temp:]

    # Output data to new filepath as CSV
    df.to_csv(new_filepath, index=False)

    # Outputs message and new filepath to terminal
    print('Cleaned file exported to: ' + new_filepath)
