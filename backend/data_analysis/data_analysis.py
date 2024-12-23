import pandas as pd
from database.db_setup import get_database
from datetime import date, timedelta

NUMERIC_COLUMNS = ["price", "sqft", "bathrooms", "bedrooms", "price/sqft"]
HOUSING_DATA_DB = get_database()

def analyze_data():
    df = initalize_df()
    
    findings = [
        king_co_averages := { "king_co_averages": find_averages(df, "King County") },
        city_averages := { "city_averages":find_city_averages(df) },
        correlations := { "correlations":find_correlations(df) },
        king_co_best_valued_listings := {"king_co_best_valued_listings": find_lowest_price_per_sqft(df, "King County")},
        best_valued_listings_per_city :={ "lowest_price/sqft_per_city": find_lowest_cities_price_per_sqft(df) },
        price_frequency_per_city := { "city_price_categories": find_cities_price_category_frequency(df) }
    ]
    
    update_analysis_findings(findings)
        
def initalize_df():  
    try:
        housing_data = HOUSING_DATA_DB
        
        cleaned_king_co_listings_data = housing_data.cleaned_king_co_listings_data
        
        cleaned_data = cleaned_king_co_listings_data.find()
        df = pd.DataFrame(list(cleaned_data))
        
        if '_id' in df.columns:
                df = df.drop(columns=['_id'])
        return df

    except Exception as e:
        print(f"An Error Occured: {e}")
        
    return pd.DataFrame()

def find_averages(df, region=None):
    stats = df[NUMERIC_COLUMNS].agg(["mean", "median", "std"]).transpose()
    stats.columns = [f"{stat}" for stat in stats.columns]  
    averages = stats.to_dict(orient="index")  

    averages_flat = {"region": region}
    for col, values in averages.items():
        for stat, value in values.items():
            averages_flat[f"{col}_{stat}"] = value

    return averages_flat

def find_city_averages(df):
    city_avgs = df.groupby("city")[NUMERIC_COLUMNS].agg(["mean", "median", "std"])

    city_avgs.columns = [f"{col}_{stat}" for col, stat in city_avgs.columns]

    city_avgs = city_avgs.reset_index()
    city_avgs = city_avgs.rename(columns={"city": "region"})
    
    return city_avgs.to_dict(orient="records")


def find_correlations(df):
    corr_dict = df[NUMERIC_COLUMNS].corr().round(3).to_dict()
    
    keys = list(corr_dict.keys())
    matrix = [[corr_dict[row].get(col, None) for col in keys] for row in keys]
    return  {"keys": keys, "matrix": matrix} 

def find_lowest_price_per_sqft(df, region=None):
    two_weeks_ago = date.today() - timedelta(weeks=2)
    weekly_df = df[df['date'].dt.date >= two_weeks_ago]

    top_5 = {
        "region": region
        }
    
    weekly_df = df.sort_values(by="price/sqft")
    top_5["listings"] = weekly_df.head(5).to_dict(orient="records")
    
    return top_5

def find_lowest_cities_price_per_sqft(df):
    
    lowst_cities = []
    cities_df = df.groupby("city")
   
    for city_name, city_data in cities_df:
       lowst_cities.append(find_lowest_price_per_sqft(city_data, city_name))
       
    return lowst_cities 

def find_cities_price_category_frequency(df):
    city_price_categories = []
    cities_df = df.groupby("city")
    
    for city_name, city_data in cities_df:
        price_category_sum = city_data["price_category"].value_counts().to_dict()
        price_category_sum["city"] = city_name
        city_price_categories.append(price_category_sum)
        
    return city_price_categories

def ensure_region_exists(region, collection):
    query = {"_id": "price_trends", "regions.region": region}
    if not collection.find_one(query):
        collection.update_one(
            {"_id": "price_trends"},
            {"$addToSet": {"regions": {"region": region, "price_trends": []}}},
            upsert=True,
        )

def update_average_trend(all_averages):
    try:    
        king_co_housing_findings = HOUSING_DATA_DB.king_co_housing_findings
        today = date.today().isoformat()
         
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


        
def update_analysis_findings(findings):
    try:
        king_co_housing_findings = HOUSING_DATA_DB.king_co_housing_findings

        query_keys = {
            "king_co_averages": lambda f: {"_id": "king_co_averages"},
            "city_averages": lambda f: {"_id": "city_averages"},
            "correlations": lambda f: {"_id": "correlations"},
            "king_co_best_valued_listings": lambda f: {"_id": "king_co_best_valued_listings"},
            "lowest_price/sqft_per_city": lambda f: {"_id": "lowest_price/sqft_per_city"},
            "city_price_categories": lambda f: {"_id": "city_price_categories"}
        }

        for finding in findings:
            query = next((func(finding) for key, func in query_keys.items() if key in finding), {"_id": "unknown"})

            king_co_housing_findings.update_one(query, {"$set": finding}, upsert=True)
            
        all_averages = [findings[0]["king_co_averages"]] + findings[1]["city_averages"]
        update_average_trend(all_averages)

        print("Findings updated in DB successfully!")

    except Exception as e:
        print(f"Data could not be updated in DB: {e}")
    
        
