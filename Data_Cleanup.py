"""

Master data cleaning script
    - Called from DF scripts to clean data read in from CSV files.
    - Currenty supports:
        Google Maps Export CSV (PhantomBuster)
        SN Search Exort CSV (PhantomBuster)

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
# TOODO
#   * only supports google maps and SN search result csv files!
def data_cleanup(df):
    # Check name of first column to determine file type
    if df.columns[0] == 'placeUrl':
        df = google_maps_ceanup(df)
    elif df.columns[0] == 'profileUrl':
        df = sn_search_cleanup(df)
    else:
        # No change to the data frame
        print('NOTE: Unfamilier file type or already clean.')
    # return the updated dataframe
    return df

# function version of previous Google_Maps_Cleanup script
def google_maps_ceanup(df):
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
