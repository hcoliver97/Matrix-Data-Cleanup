"""

Master data cleaning script.
Handles decidng what kind of file it is and cleaning it.
Takes dataframe as input argument

"""

if __name__ == '__main__':
    data_cleanup()

def data_cleanup(df):
    if df.columns[0] == 'placeUrl':
        google_maps_ceanup(df)
    elif df.columns[0] == 'profileUrl':
        sn_search_cleanup(df)
    else:
        print('Unfamilier filetype or already cleaned.')

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

def sn_search_cleanup(df):
    # Keep only
    #   profileUrl, firstName, lastName, companyName, title, companyId, summary,
    #   location duration pastRole pastCompany
    deletion_list = ['name', 'companyUrl', 'pastCompanyUrl', \
        'connectionDegree','profileImageUrl', 'sharedConnectionsCount', 'vmid', \
        'isPremium', 'query', 'timestamp']
    # Deletes columns specified in list if they exist, ignores error otherwise
    df = df.drop(deletion_list, axis = 1, errors = 'ignore')
