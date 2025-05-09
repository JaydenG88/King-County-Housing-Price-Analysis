import pandas as pd
from database.db_setup import get_database
from datetime import date, timedelta, datetime

NUMERIC_COLUMNS = ["price", "sqft", "bathrooms", "bedrooms", "price/sqft"]

# Main function that calls analysis functions and stores data to MongoDB
def analyze_data():
    housing_data_db = get_database()
    df = initalize_df(housing_data_db)
    # Stores the main findings and function calls
    findings = [
        averages := { "averages":find_regions_averages(df) + [find_king_co_averages(df)] },
        correlations := { "correlations":find_correlations(df) },
        best_valued_listings := {"best_valued_listings": (find_lowest_regions_price_per_sqft(df)) },
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
def find_king_co_averages(df):
    recent_listings_df = valid_listings_date(df)
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
def find_regions_averages(df):
    # Performs averages operations 
    recent_listings_df = valid_listings_date(df)
    city_avgs = recent_listings_df.groupby("city")[NUMERIC_COLUMNS].agg(["mean", "median", "std"])
    current_time = datetime.now().isoformat()

    # Formats column names
    city_avgs.columns = [f"{col}_{stat}" for col, stat in city_avgs.columns]

    city_avgs = city_avgs.reset_index()
    city_avgs = city_avgs.rename(columns={"city": "region"})
    city_avgs["date"] = current_time
    return city_avgs.to_dict(orient="records")

# Returns dataframe with recent listings dating back to 4 weeks
def valid_listings_date(df):
    df = df.copy()  
    df['date'] = pd.to_datetime(df['date'])
    valid_date = pd.Timestamp.now() - timedelta(weeks=4)
    recent_listings_df = df[df["date"] >= valid_date]
    
    return recent_listings_df


# Creates correlation matrix of all numeric columns
def find_correlations(df):
    corr_dict = df[NUMERIC_COLUMNS].corr().round(3).to_dict()
    
    keys = list(corr_dict.keys())
    matrix = [[corr_dict[row].get(col, None) for col in keys] for row in keys]
    return  {"keys": keys, "matrix": matrix} 

# Helper function that finds top 5 listings with the lowest price/sqft in a region
def find_lowest_price_per_sqft(df, region=None):
    recent_df = valid_listings_date(df)

    top_5 = {
        "region": region
        }
    
    recent_df = recent_df.sort_values(by="price/sqft")
    top_5["listings"] = recent_df.head(5).to_dict(orient="records")
    
    return top_5

# Finds top 5 listings with lowest price/sqft for all regions
def find_lowest_regions_price_per_sqft(df):
    
    recent_df = valid_listings_date(df)
    lowst_cities = []
    cities_df = recent_df.groupby("city")
   
    for city_name, city_data in cities_df:
       lowst_cities.append(find_lowest_price_per_sqft(city_data, city_name))
    lowst_cities.append(find_lowest_price_per_sqft(recent_df, "King County"))
       
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
                "price/sqft_mean": averages["price/sqft_mean"],
                "price/sqft_median": averages["price/sqft_median"],
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
            
            # Adds a new date entry for the region if today's average trends are not already stored
            if not existing_entry:
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
            query = next((func(finding) for key, func in query_keys.items() if key in finding), {"_id": "unknown"})

            king_co_housing_findings.update_one(query, {"$set": finding}, upsert=True)
        
        # Updates the average trends    
        update_average_trend(findings[0]["averages"], database)

        print("Findings updated in DB successfully!")

    except Exception as e:
        print(f"Data could not be updated in DB: {e}")
    
        
