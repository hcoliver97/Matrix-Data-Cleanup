"""

Master data cleaning script
    - Called from DF scripts to clean data read in from CSV files.
    - Currenty supports:
        Google Maps Export CSV  (PhantomBuster)
        SN Search Exort CSV     (PhantomBuster)
        Email Open Log CSV      (Constant Contact)
        Click Log CSV           (Constant Contact)

    - Drops columns with redundant info/errors and returns formatted DataFrame
        to be incorporated into Lead DataFrames

    TODO:
        * handle more filetypes
        * handle being called from commandline alone
        * handle exporting cleaned data to CSV

"""
# Specifies main method
if __name__ == '__main__':
    data_cleanup()

# Control flow method to determine filetype and call appropriate
# cleanup function and update dataframe with results
def data_cleanup(df):
    # Check name of first column to determine file type
    if df.columns[0] == 'placeUrl':
        df = google_maps_cleanup(df)
    elif df.columns[0] == 'profileUrl':
        df = sn_search_cleanup(df)
    elif df.columns[0] == 'Email address':
        df = constant_contact_cleanup(df)
    else:
        # No change to the data frame
        print('NOTE: Unfamilier file type or already clean.')
    # return the updated dataframe
    return df

# function version of previous Google_Maps_Cleanup script
def google_maps_cleanup(df):
    # Take in DataFrame of google maps export to clean
    # Keeping only columns:
    # placeUrl, title, category, address, website, phoneNumber, openingHours,
    # isClaimed, latitude, and longitude.
    # List of columns to delete
    deletion_list = ['subtitle', 'rating', 'reviewCount', \
            'attributes', 'plusCode', 'imgUrl', 'query', 'timestamp',\
            'tuesday','wednesday','thursday','friday','saturday',\
            'sunday','monday']
    # Deletes columns specified in list if they exist, ignores otherwise
    df = df.drop(deletion_list, axis = 1, errors = 'ignore')
    # Keep only results (rows) with no errors (error is null)
    df = df[df.error.isna()]
    # Drop error column since every row is error free now
    df = df.drop(['error'], axis = 1, errors = 'ignore')
    # Keep only results (rows) with a website (website is not null)
    df = df[df.website.notna()]
    return df

# function version of previous SN_Search_Cleanup script
def sn_search_cleanup(df):
    # Keep only columns:
    # profileUrl, firstName, lastName, companyName, title, companyUrl, summary,
    # location, duration, pastRole, pastCompany
    deletion_list = ['name', 'companyId', 'pastCompanyUrl', \
        'connectionDegree','profileImageUrl', 'sharedConnectionsCount', 'vmid', \
        'isPremium', 'query', 'timestamp']
    # Deletes columns specified in list if they exist, ignores error otherwise
    df = df.drop(deletion_list, axis = 1, errors = 'ignore')
    # Keep only results (rows) with no errors (error is null)
    df = df[df.error.isna()]
    # Drop error column since every row is error free now
    df = df.drop(['error'], axis = 1, errors = 'ignore')
    # return updated dataframe
    return df

# function to clean up Constant Contact E-blast CSV
def constant_contact_cleanup(df):
    # if last column is 'opened at' call open_log_cleanup
    # if the last column is 'clicked at' call click_log_cleanup
    if df.columns[-1] == 'Opened At':
        df = open_log_cleanup(df)
    elif df.columns[-1] == 'Clicked At':
        df = click_log_cleanup(df)
    else:
        print('NOTE: Unfamilier CC file type.')

    # return updated dataframe
    return df

# Functions clean constant contact open logs
def open_log_cleanup(df):
    # Keep only columns:
    # Email address, First name, Last name, Company, Job title, Email status,
    # Phone - mobile, Phone - work, Street address line 1 - Home, City - Home,
    # State/Province - Home, Zip/Postal Code - Home, Website, Industry,
    # Annual Revenue, number of employees, Tags, Opened At
    deletion_list = ['Email permission status', 'Email update source',\
    'Confirmed Opt-Out Date', 'Confirmed Opt-Out Source',\
    'Confirmed Opt-Out Reason','Salutation','Initial Email Status',\
    'Prospect Location', 'Location of Contact', 'Infogroup ID', 'Gender',\
    'Email Lists', 'Source Name', 'Created At', 'Updated At']

    # Deletes columns specified in list if they exist, ignores error otherwise
    df = df.drop(deletion_list, axis = 1, errors = 'ignore')

    return df

# Function that cleans constant contact click logs
def click_log_cleanup(df):
    # Keep only columns:
    # Email address, First name, Last name, Tags, Clicked Link Address, Opened At
    deletion_list = ['First name', 'Last name', 'Company', 'Job title',\
    'Email status','Email permission status','Email update source',\
    'Phone - mobile', 'Phone - work', 'Street address line 1 - Home',\
    'City - Home', 'State/Province - Home', 'Zip/Postal Code - Home',
    'Country - Home', 'Website', 'Industry', 'Initial Email Status',\
    'Company LI','LinkedIn URL','number of employees','Prospect Location',\
    'Location of Contact','Tags','Email Lists','Source Name','Created At',\
    'Updated At']
    # Deletes columns specified in list if they exist, ignores error otherwise
    df = df.drop(deletion_list, axis = 1, errors = 'ignore')


    return df
