from database.db_setup import get_database
from pymongo.errors import PyMongoError

FINDINGS_COLLECTION = get_database().king_co_housing_findings

def get_averages(metric, type):
    metric = metric.lower()
    type = type.lower()
    
    try:
        city_averages = list(FINDINGS_COLLECTION.find({"_id": "averages"}))
        print(f"TEST:{city_averages}")
        key = f"{metric}_{type}"
        
        return [
            {"region": entry["region"], "value": entry.get(key)}
            for entry in city_averages[0].get("averages", [])
            if key in entry
        ]
        
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
    
    
def get_lowest_price_per_sqft(region):
    region = str(region).lower().title()

    try:
        lowest = FINDINGS_COLLECTION.find_one(
            {"best_valued_listings": {"$elemMatch": {"region": region}}}
             ,{"best_valued_listings.$": 1, "_id": 0}
        )
        return lowest.get("best_valued_listings") if lowest else None
    except PyMongoError as e:
        print(f"Error fetching lowest price per sqft by city: {e}")
        return None

def get_price_category_frequency(region):
    try:
        price_category_frequency = list(FINDINGS_COLLECTION.find({"price_category_frequency" : {"$elemMatch": {"region": region}}}
             ,{"price_category_frequency.$": 1, "_id": 0}
        ))
        return price_category_frequency
    except PyMongoError as e:
        print(f"Error fetching price category frequency: {e}")
        return None

def get_price_trends_by_city(region):
    region = str(region).lower().title()
    
    try:
        regions = FINDINGS_COLLECTION.find_one(
            {"regions.region": region},
            {"regions.$": 1}
        )
        
        region = regions.get("regions")[0] if regions else None
        return region
    
    except PyMongoError as e:
        print(f"Error fetching price trends by region: {e}")
        return None

