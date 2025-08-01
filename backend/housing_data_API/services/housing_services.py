from database.db_setup import get_database
from pymongo.errors import PyMongoError
from datetime import datetime

FINDINGS_COLLECTION = get_database().king_co_housing_findings

def get_averages(metric, type):
    metric = metric.lower()
    type = type.lower()
    
    try:
        city_averages = list(FINDINGS_COLLECTION.find({"_id": "averages"}))
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
        correlations_doc = list(FINDINGS_COLLECTION.find({"_id": "correlations"}))
        keys = correlations_doc[0]["correlations"]["keys"]
        matrix = correlations_doc[0]["correlations"]["matrix"]
        
        correlations = {
            "keys": keys,
            "matrix": matrix
        }
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
        return lowest.get("best_valued_listings")[0].get("listings") if lowest else None
    except PyMongoError as e:
        print(f"Error fetching lowest price per sqft by city: {e}")
        return None

def get_price_category_frequency(region):
    region = region.lower().title()
    try:
        city_price_categories = FINDINGS_COLLECTION.find_one({
            "city_price_categories" : {"$elemMatch": {"city": region}}},
            {"city_price_categories.$": 1, "_id": 0})
        
        category_frequency = city_price_categories.get("city_price_categories")[0] if city_price_categories else None
        formatted = [{"category": k, "value": v} for k, v in category_frequency.items() if k != "city"]
        return formatted
    
    except PyMongoError as e:
        print(f"Error fetching price category frequency: {e}")
        return None

def get_price_trends(region, metric, type):
    metric = str(metric).lower()
    type = str(type).lower()
    region = str(region).lower().title()
    
    try:
        regions = FINDINGS_COLLECTION.find_one(
            {"regions.region": region},
            {"regions.$": 1}
        )
        
        region = regions.get("regions")[0] if regions else None
        if not region:
            return None
        
        return [
            {
                "date": entry["date"],
                "value": entry.get(f"{metric}_{type}")
            }
            for entry in region.get("price_trends", [])
            if f"{metric}_{type}" in entry
        ] if region else None
        
    except PyMongoError as e:       
        print(f"Error fetching price trends: {e}")
        return None
        
def get_regions():
    try:
        regions = list(FINDINGS_COLLECTION.distinct("regions.region"))
        
        if "King County" in regions:
            regions.remove("King County")
            regions.insert(0, "King County")
            
        return regions
        
    except PyMongoError as e:
        print(f"Error fetching regions: {e}")
        return None

def get_date():
    try:
        # Gets most recent date from price trends
        overtime = get_price_trends("king county", "price", "median")
        date = overtime[len(overtime) - 1]["date"] if overtime else None
        
        if date:
            formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%B %d, %Y")
            return formatted_date
        
        return None
    except PyMongoError as e:
        print(f"Error fetching date: {e}")
        return None        