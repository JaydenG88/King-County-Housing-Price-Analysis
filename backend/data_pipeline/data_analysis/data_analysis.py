import pandas as pd
from database.db_setup import get_database
from datetime import date, timedelta, datetime

NUMERIC_COLUMNS = ["price", "sqft", "bathrooms", "bedrooms", "price_per_sqft"]

# Main function that calls analysis functions and stores data to MongoDB
# @param weeks is how far back "recent" listings go for averages/best-valued calculations.
# Normally 4 (fits the weekly ETL cadence); widen it for a one-off recompute from stale
# historical data (e.g. recovering coverage after the pipeline was broken for months).
def analyze_data(weeks=4):
    housing_data_db = get_database()
    df = initalize_df(housing_data_db)
    # Stores the main findings and function calls
    findings = [
        averages := { "averages":find_regions_averages(df, weeks) + [find_king_co_averages(df, weeks)] },
        correlations := { "correlations":find_correlations(df) },
        best_valued_listings := {"best_valued_listings": (find_lowest_regions_price_per_sqft(df, weeks)) },
        price_frequency_per_city := { "city_price_categories": find_cities_price_category_frequency(df) }
    ]

    update_analysis_findings(findings, housing_data_db)

# Initializes the dataframe from cleaned data collection
def initalize_df(database):  
    try:
        cleaned_king_co_listings_data = database.cleaned_king_co_listings_data
        
        cleaned_data = cleaned_king_co_listings_data.find()
        df = pd.DataFrame(list(cleaned_data))
        
        if '_id' in df.columns:
                df = df.drop(columns=['_id'])
        return df

    except Exception as e:
        print(f"An Error Occured: {e}")
        
    return pd.DataFrame()

# Finds bi-weekly averages for each numeric category for all of King County
def find_king_co_averages(df, weeks=4):
    recent_listings_df = valid_listings_date(df, weeks)
    current_time = datetime.now().isoformat()
    
    # Performs averages operations using pandas aggregation method 
    king_co_stats = recent_listings_df[NUMERIC_COLUMNS].agg(["mean", "median"]).transpose()
    king_co_stats.columns = [f"{stat}" for stat in king_co_stats.columns]  
    averages = king_co_stats.to_dict(orient="index")  

    # Formats column names
    averages_flat = {"region": "King County"}
    for col, values in averages.items():
        for stat, value in values.items():
            averages_flat[f"{col}_{stat}"] = value
    
    averages_flat["date"] = current_time
    return averages_flat

# Finds bi-weekly averages for each city in King County
def find_regions_averages(df, weeks=4):
    # Performs averages operations
    recent_listings_df = valid_listings_date(df, weeks)
    city_avgs = recent_listings_df.groupby("city")[NUMERIC_COLUMNS].agg(["mean", "median", "std"])
    current_time = datetime.now().isoformat()

    # Formats column names
    city_avgs.columns = [f"{col}_{stat}" for col, stat in city_avgs.columns]

    city_avgs = city_avgs.reset_index()
    city_avgs = city_avgs.rename(columns={"city": "region"})
    city_avgs["date"] = current_time
    return city_avgs.to_dict(orient="records")

# Returns dataframe with listings dating back the given number of weeks (default 4)
def valid_listings_date(df, weeks=4):
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])
    valid_date = pd.Timestamp.now() - timedelta(weeks=weeks)
    recent_listings_df = df[df["date"] >= valid_date]

    return recent_listings_df


# Creates correlation matrix of all numeric columns
def find_correlations(df):
    corr_dict = df[NUMERIC_COLUMNS].corr().round(3).to_dict()
    
    keys = list(corr_dict.keys())
    matrix = [[corr_dict[row].get(col, None) for col in keys] for row in keys]
    return  {"keys": keys, "matrix": matrix} 

# Helper function that finds top 5 listings with the lowest price/sqft in a region
def find_lowest_price_per_sqft(df, region=None, weeks=4):
    recent_df = valid_listings_date(df, weeks)

    top_5 = {
        "region": region
        }

    recent_df = recent_df.sort_values(by="price_per_sqft")
    top_5["listings"] = recent_df.head(5).to_dict(orient="records")

    return top_5

# Finds top 5 listings with lowest price/sqft for all regions
def find_lowest_regions_price_per_sqft(df, weeks=4):

    recent_df = valid_listings_date(df, weeks)
    lowst_cities = []
    cities_df = recent_df.groupby("city")

    for city_name, city_data in cities_df:
       lowst_cities.append(find_lowest_price_per_sqft(city_data, city_name, weeks))
    lowst_cities.append(find_lowest_price_per_sqft(recent_df, "King County", weeks))
       
    return lowst_cities 

# Finds price category frequency for each city
def find_cities_price_category_frequency(df):
    city_price_categories = []
    cities_df = df.groupby("city")
    
    for city_name, city_data in cities_df:
        price_category_sum = city_data["price_category"].value_counts().to_dict()
        price_category_sum["city"] = city_name
        city_price_categories.append(price_category_sum)
        
    return city_price_categories

# Queries database to ensure location is existing
def ensure_region_exists(region, collection):
    query = {"_id": "price_trends", "regions.region": region}
    if not collection.find_one(query):
        collection.update_one(
            {"_id": "price_trends"},
            {"$addToSet": {"regions": {"region": region, "price_trends": []}}},
            upsert=True,
        )

# Stores and updates the historical averages for all regions
def update_average_trend(all_averages, housing_data_db):
    try:    
        king_co_housing_findings = housing_data_db.king_co_housing_findings
        today = date.today().isoformat()
         
        # Finds the averages for each location
        for averages in all_averages:
            entry = {
                "price_mean": averages["price_mean"],
                "price_median": averages["price_median"],
                "price_per_sqft_mean": averages["price_per_sqft_mean"],
                "price_per_sqft_median": averages["price_per_sqft_median"],
                "date": today
            } 
            
            region = averages["region"]
            query = {"_id": "price_trends"}   
            
            ensure_region_exists(region, king_co_housing_findings)
            
            # Query for the region's average price trends
            existing_entry_query = {
                "_id": "price_trends",
                "regions": {
                    "$elemMatch": {
                        "region": region,
                        "price_trends.date": today
                    }
                }
            }
            existing_entry = king_co_housing_findings.find_one(existing_entry_query)
            
            if existing_entry:
                # Update the existing entry for today
                update = {
                    "$set": {
                        "regions.$[r].price_trends.$[pt]": entry
                    }
                }
                array_filters = [
                    {"r.region": region},
                    {"pt.date": today}
                ]
                
                king_co_housing_findings.update_one(
                    query, update, array_filters=array_filters
                )
            else:
                # Add a new entry if no entry exists for today
                update = { 
                    "$addToSet": {"regions.$[r].price_trends": entry}
                }
                array_filters = [{"r.region": region}]
                
                king_co_housing_findings.update_one(
                    query, update, array_filters=array_filters
                )
            
        print(f"Price Trends successfully updated!")
    except Exception as e:
        print(f"price_trends could not be updated: {e}")

# Fields holding a per-region/city array in each finding, and the key identifying each entry.
# A location missing from this pipeline run must not erase other locations' existing entries.
ARRAY_FIELD_KEYS = {
    "averages": "region",
    "best_valued_listings": "region",
    "city_price_categories": "city"
}

# Merges new per-region/city entries into an existing array, replacing entries that share
# an identifying key and keeping existing entries this run didn't touch
def merge_array_field(existing_array, new_array, id_key):
    merged = {entry.get(id_key): entry for entry in (existing_array or [])}
    for entry in new_array:
        merged[entry.get(id_key)] = entry
    return list(merged.values())

# Updates and stores all findings to the database
def update_analysis_findings(findings, database):
    try:
        king_co_housing_findings = database.king_co_housing_findings

        # Creates query keys for each document in the findings collection
        query_keys = {
            "averages": lambda f: {"_id": "averages"},
            "correlations": lambda f: {"_id": "correlations"},
            "best_valued_listings": lambda f: {"_id": "best_valued_listings"},
            "city_price_categories": lambda f: {"_id": "city_price_categories"}
        }

        # Updates and executes lambda functions for each finding
        for finding in findings:
            field = next((key for key in query_keys if key in finding), None)
            query = query_keys.get(field, lambda f: {"_id": "unknown"})(finding)

            if field in ARRAY_FIELD_KEYS:
                id_key = ARRAY_FIELD_KEYS[field]
                existing_doc = king_co_housing_findings.find_one(query)
                finding = {field: merge_array_field(
                    existing_doc.get(field) if existing_doc else None,
                    finding[field],
                    id_key
                )}

            king_co_housing_findings.update_one(query, {"$set": finding}, upsert=True)

        # Updates the average trends
        update_average_trend(findings[0]["averages"], database)

        print("Findings updated in DB successfully!")

    except Exception as e:
        print(f"Data could not be updated in DB: {e}")
    
        
