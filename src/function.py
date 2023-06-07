#function.py

def get_distance(item_zip, buyer_zip):
    """
    We are going to use the package mpu and uszipcode to imporve the speed of calculating the distance between buyer and seller by using zip code. 
    These 2 packages make the speed of calculation much faster compare with using the geopy package
    """
    if item_zip is not None and buyer_zip is not None:
        search = SearchEngine()
        item_location = search.by_zipcode(item_zip[0:5])
        buyer_location =search.by_zipcode(buyer_zip[0:5])
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

