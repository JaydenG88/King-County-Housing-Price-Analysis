import pandas as pd
import numpy as np
from database.db_setup import get_database

NUMERIC_COLUMNS = ["price", "sqft", "bathrooms", "bedrooms", "price/sqft"]
HOUSING_DATA_DB = get_database()


def analyze_data():
    df = initalize_df()
    king_co_averages = find_averages(df)
    city_averages = find_city_averages(df)
    correlations = find_correlations(df)
    
    print(king_co_averages)
    print(city_averages)
    print(correlations)
        
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

def find_averages(df, group=None):
    averages = {
        "Group": group
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
    return {"keys": keys, "matrix": matrix}

def store_data_to_DB(findings):
    try:
        king_co_housing_findings = HOUSING_DATA_DB.king_co_housing_findings
        king_co_housing_findings.insert_many(findings)

        print("Findings saved to DB successfully!")
        
    except Exception as e:
        print(f"Data could not be saved to DB: {e}")
        
analyze_data()