"""

Master data cleaning script.
Handles decidng what kind of file it is and cleaning it.
Takes dataframe as input argument

"""
import Google_Maps_Cleanup
import SN_Search_Cleanup

if __name__ == '__main__':
    data_cleanup()

def data_cleanup(data):
    print(data.columns[1])
    if data.columns[1] == 'placeUrl':
        Google_Maps_Cleanup.clean(data)
    elif data.columns[1] == 'profileUrl':
        SN_Search_Cleanup.clean(data)
    else:
        print('unfamilier filetype or already cleaned ')
