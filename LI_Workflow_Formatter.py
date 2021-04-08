'''

Formatting LinkedIn Leads for new workflow sheet

Input: Filepath to CSV file containing data from LinkedHelper

Output: File containing cleaned data ready to upload to
        Workflow Google Sheet. File will have same name as original but
        '_cleaned' at the end of the file name.

This script deletes unnecessary columns and arranges the remaining columns to
fit the LI Workflow sheet format. Keeps info for 3 organizations, basic lead info,
tags, etc as shown in column_names list.

This does not distinguish between current and past organizations!
Only formats the given data for upload.

TODO:
    - Process and condense some of the columns like start and end date into
    neater format 'MM/DD/YYYY - Present' or 'MM/DD/YYY - MM/DD/YYYY' in one column?
    - Make this modular part of Data_Cleanup.py

'''

# Pandas - data analysis module for python
import sys
import pandas as pd

# Read contents of csv file specified in commandline input
filepath = sys.argv[1]
data = pd.read_csv(filepath)

# Convert CSV data to Data Frame (Pandas object) for easier manipulation
df = pd.DataFrame(data)

# List of columns to delete
deletion_list = ['id', 'current_company', 'current_company_position',\
    'headline','public_id','hash_id', 'member_id', 'sn_member_id',\
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
    'organization_location_1','organization_location_2','organization_location_3',\
    'organization_location_4','organization_4','organization_url_4',\
    'organization_title_4','organization_start_4','organization_end_4',\
    'organization_website_4','languages', 'twitters', 'phone_type_1',\
    'phone_type_2','mutual_first_fullname', 'mutual_second_fullname', \
    'original_mutual_first_fullname', 'original_mutual_second_fullname', \
    'custom_mutual_first_fullname','custom_mutual_second_fullname','followers',\
    'member_distance','network_info_connection_count', 'network_info_following',\
    'third_party_email_1','third_party_email_source_1', \
    'third_party_email_is_valid_1', 'third_party_email_2',\
    'third_party_email_source_2', 'third_party_email_source_3', \
    'third_party_email_is_valid_2', 'third_party_email_3',\
    'third_party_email_is_valid_3', 'mutual_count','language_1',\
    'language_proficiency_1','language_2',\
    'language_proficiency_2','language_3','language_proficiency_3']
# Deletes columns specified in list if they exist, ignores error otherwise
df = df.drop(deletion_list, axis = 1, errors = 'ignore')

# List of columns in order that appears on workflow sheet
column_names = ['connected_at', 'profile_url','tags','email','first_name',\
	'last_name','location_name','industry',	'organization_1','organization_url_1',\
    'organization_title_1',	'organization_start_1',	'organization_end_1',\
    'organization_website_1','organization_2','organization_url_2',\
    'organization_title_2',	'organization_start_2',	'organization_end_2',\
    'organization_website_2','organization_3','organization_url_3',	\
    'organization_title_3','organization_start_3','organization_end_3',\
    'organization_website_3','skills','phone_1','phone_2','website_1','website_2',\
    'website_3']

# Re-order the columns according to above list.
# Moves Connected At and Tags to position A and C
df = df.reindex(columns = column_names)

# Reformat the date in organization start and end columns
# Loop through each row of DF
for index in df.index:
    # Loop through organizations 1 - 3
    for i in [1, 2, 3]:
        # convert start date from YYYY.MM to YYYY-MM so that it is in a string
        # format that google sheets will recognize.
        # entries with only a year will be formatted yyyy.0
        start_date = df['organization_start_'+str(i)][index]
        # Check if start date cell has a number in it
        if start_date>0:
            # split the date into start_date = [year, month]
            start_date = str(start_date).split('.')
            # If the month (index 0) is 0, only keep year
            if(start_date[1]=='0'):
                start_date = start_date[0]
            else:
                # If there is a month and year, join them into one string
                # start_date = 'year-month'
                start_date = '-'.join(start_date)
        else:
            # No start date, emotpty org i fields so all orgs have been checked
            # Exit loop, continue to next row.
            break

        end_date = df['organization_end_'+str(i)][index]
        # Check if start date cell has a number in it
        if end_date>0:
            # split the date into start_date = [year, month]
            end_date = str(end_date).split('.')
            # If the month (index 0) is 0, only keep year
            if(end_date[1]=='0'):
                end_date = end_date[0]
            else:
                # If there is a month and year, join them into one string
                # end_date = 'year-month'
                end_date = '-'.join(end_date)
        else:
            # if no end date exists, the job is a current job, add 'Present'
            # as end date
            end_date = 'Present'

        # Save formatted date info to the DF
        df['organization_start_'+str(i)][index] = start_date
        df['organization_end_'+str(i)][index] = end_date


# Generate new filepath to store the cleaned file
# [original file name]_Cleaned.csv in same directory as original file path
temp = filepath.find('.csv')
new_filepath = filepath[:temp] + '_Cleaned' + filepath[temp:]

# Output data to new filepath as CSV
df.to_csv(new_filepath, index=False)

# Prints summary and location of output file.
print('Cleaned file exported to: ' + new_filepath)
