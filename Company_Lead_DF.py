"""
Sample Script to Convert Company Lead Info CSVs into one big CSV

 - read in csv file to process
 - check row if unique in business_lead_df


"""
import sys
import pandas as pd

# Create business lead data frame --> we want to keep adding to existing csv
# so this needs to be if csv file for existing business lead df isnt existing
bl_fields = ['title','sector', 'website', 'phoneNumber', 'address',\
        'linkedInUrl', 'size', 'revanue', 'contactPerson']

business_lead_df = pd.DataFrame(columns = bl_fields)

# Read in iput files, make sure to check if cleaned or run cleaning module on it
input_filepath = sys.argv[1]

input_data = pd.read_csv(input_filepath)
input_df = pd.DataFrame(input_data)

# check if adding duplicate values
# Probbaly need to do this different or use unique value function in concat
# ouput the ones that do exist to terminal for check and dismiss?
for entry in input_df:
    if input_df.entry.title in business_lead_df.title:
        if input_df.entry.phoneNumber in business_lead_df.phoneNumber:
            # This entry exists in lead DB already, drop it
            input_df.entry.drop()
        else:
            # Same name, different business
    else:
        # Business not yet in database

# Once we have dropped all entries that are duplicates we can merge dfs
pd.concat([business_lead_df, input_df], ignore_index = True)

# Public processed dataframe to CSV file
