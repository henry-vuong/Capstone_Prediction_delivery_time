import pandas as pd
import numpy as np
import string
import mpu
from uszipcode import SearchEngine
from sklearn.preprocessing import OrdinalEncoder
import sys

def process_text():
    

    inputfile = sys.argv[1]
    outputfile = sys.argv[2]

    # Read in the data
    print("\tReading data...")
    data = pd.read_csv('../data/raw/ebayShort.csv')

    print("\convert b2c_c2c to binary...")
    # convert b2c_c2c column to binary
    data['b2c_c2c'] = np.where(data['b2c_c2c']== "B2C", 1, 0)

    print("\Convert weight in kg to lb... ")
    data["weight"]= np.where(data["weight_units"==1, data["weight"], data["weight"]*2.20462])
    #Then drop the weight_units columns
    data.drop(columns='weight_units', axis=1, inplace=True)

    #ordinal encoding 
    oe_package= OrdinalEncoder(categories=[['NONE', 'LETTER', 'LARGE_ENVELOPE',
                                         'LARGE_PACKAGE', 'PACKAGE_THICK_ENVELOPE']])
    df_ebay['package_size']=oe_package.fit_transform(pd.DataFrame(df_ebay['package_size'])) 

    # calculate distance
    item_zip= df_ebay['item_zip']
    buyer_zip= df_ebay['buyer_zip']


    """
    We are going to use the package mpu and uszipcode to imporve the speed of calculating the distance between buyer and seller by using zip code. 
    These 2 packages make the speed of calculation much faster compare with using the geopy package
    """
    print('C\alculate distance ....')
    if item_zip is not None and buyer_zip is not None:
        search_location = SearchEngine()
        item_location = search_location.by_zipcode(item_zip[0:5])
        buyer_location =search_location.by_zipcode(buyer_zip[0:5])
        if item_location is None or buyer_location is None:
            return None
        else:
            lat1 =item_location.lat
            long1 =item_location.lng
            lat2 =buyer_location.lat
            long2 =buyer_location.lng
            if lat1 is None or lat2 is None or long1 is None or long2 is None:
                return None
            return mpu.haversine_distance((lat1,long1),(lat2,long2)) 
    else:
        return None
    print('add to dataframe')
    item_zip_str = item_zip.apply(lambda x: str(x))
    buyer_zip_str = buyer_zip.apply(lambda x: str(x))
    zips = pd.concat([item_zip_str, buyer_zip_str], axis=1)
    zips['distance'] = zips.apply(lambda x: get_distance(x.item_zip, x.buyer_zip), axis=1)
    
    # Write output
    print(f"\tWriting outputfile "+outputfile)
    sms_df.to_csv(outputfile, header=True, index=False)