import pandas as pd
import numpy as np
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
    averages = {
        "region": region
    }
    
    for column in NUMERIC_COLUMNS:
        mean = df[column].mean()
        median = df[column].median()
        stdev = df[column].std()
        
        averages[f"{column}_mean"] = mean
        averages[f"{column}_median"] = median
        averages[f"{column}_stdev"] = stdev

    return averages

def find_city_averages(df):
    city_averages = []
    grouped = df.groupby("city")
    
    for city_name, city_data in grouped:
        city_averages.append(find_averages(city_data, city_name))
    
    return city_averages

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
    city_lowest = []
    cities_df = df.groupby("city")
    
    for city_name, city_data in cities_df:
       city_lowest.append(find_lowest_price_per_sqft(city_data, city_name))

    return city_lowest 

def find_cities_price_category_frequency(df):
    city_price_categories = []
    cities_df = df.groupby("city")
    for city_name, city_data in cities_df:
        price_category_sum = city_data["price_category"].value_counts().to_dict()
        price_category_sum["city"] = city_name
        city_price_categories.append(price_category_sum)
    return city_price_categories

def update_average_trend(average):
    return
        
def update_analysis_findings(findings):
    try:
        king_co_housing_findings = HOUSING_DATA_DB.king_co_housing_findings

        query_keys = {
            "king_co_averages": lambda f: {"type": "king_co_averages"},
            "city_averages": lambda f: {"type": "city_averages"},
            "correlations": lambda f: {"type": "correlations"},
            "king_co_best_valued_listings": lambda f: {"type": "king_co_best_valued_listings"},
            "lowest_price/sqft_per_city": lambda f: {"type": "lowest_price/sqft_per_city"},
            "city_price_categories": lambda f: {"type": "city_price_categories"}
        }

        for finding in findings:
            query = next((func(finding) for key, func in query_keys.items() if key in finding), {"type": "unknown"})

            king_co_housing_findings.update_one(query, {"$set": finding}, upsert=True)

        print("Findings updated in DB successfully!")

    except Exception as e:
        print(f"Data could not be updated in DB: {e}")
    
        
