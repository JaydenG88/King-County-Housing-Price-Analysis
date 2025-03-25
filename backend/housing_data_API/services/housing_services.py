from database.db_setup import get_database
from pymongo.errors import PyMongoError

FINDINGS_COLLECTION = get_database().king_co_housing_findings

def get_king_county_average():    
    try:
        king_county_average = list(FINDINGS_COLLECTION.find_one({"_id": "king_county_average"})) 
        return king_county_average
    except PyMongoError as e:
        print(f"Error fetching king county average: {e}")

def get_city_averages():
    try:
        city_averages = list(FINDINGS_COLLECTION.find({"_id": "city_averages"}))
        return city_averages
    except PyMongoError as e:
        print(f"Error fetching city averages: {e}")
        return None
        
def get_correlations():
    try:
        correlations = list(FINDINGS_COLLECTION.find({"_id": "correlations"}))
        return correlations
    except PyMongoError as e:
        print(f"Error fetching correlations: {e}")
        return None
    
def get_lowest_price_per_sqft():
    try:
        lowest_price_per_sqft = list(FINDINGS_COLLECTION.find({"_id": "king_co_best_valued_listings"}))
        return lowest_price_per_sqft
    except PyMongoError as e:
        print(f"Error fetching lowest price per sqft: {e}")
        return None
    
def get_lowest_price_per_sqft_all_city():
    try:
        lowest_price_per_sqft_by_city = list(FINDINGS_COLLECTION.find({"_id": "lowest_price/sqft_per_city"}))
        return lowest_price_per_sqft_by_city
    except PyMongoError as e:
        print(f"Error fetching lowest price per sqft by city: {e}")
        return None
def get_lowest_price_per_sqft_by_city(city):
    city = str(city).lower().title()

    try:
        lowest = FINDINGS_COLLECTION.find_one(
            {"lowest_price/sqft_per_city": {"$elemMatch": {"region": city}}}
             ,{"lowest_price/sqft_per_city.$": 1, "_id": 0}
        )
        return lowest.get("lowest_price/sqft_per_city") if lowest else None
    except PyMongoError as e:
        print(f"Error fetching lowest price per sqft by city: {e}")
        return None

def get_price_category_frequency():
    try:
        price_category_frequency = list(FINDINGS_COLLECTION.find({"_id": "price_category_frequency"}))
        return price_category_frequency
    except PyMongoError as e:
        print(f"Error fetching price category frequency: {e}")
        return None
    
def get_all_price_trends():
    try:
        price_trends = list(FINDINGS_COLLECTION.find({"_id": "price_trends"}))
        return price_trends
    except PyMongoError as e:
        print(f"Error fetching price trends: {e}")
        return None

def get_price_trends_by_city(city):
    city = str(city).lower().title()
    
    try:
        regions = FINDINGS_COLLECTION.find_one(
            {"regions.region": city},
            {"regions.$": 1}
        )
        
        region = regions.get("regions")[0] if regions else None
        return region
    
    except PyMongoError as e:
        print(f"Error fetching price trends by city: {e}")
        return None

