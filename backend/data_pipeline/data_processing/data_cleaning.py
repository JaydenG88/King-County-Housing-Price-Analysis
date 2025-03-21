import pandas as pd
import numpy as np
from scipy.stats.mstats import winsorize
from database.db_setup import get_database
from pymongo.errors import PyMongoError
from data_ingestion.scraper_config import LOCATIONS

STRING_COLUMNS = ["zip", "street_address", "state", "URL", "image", "city", "date"]
NUMERIC_COLUMNS = ["price", "sqft", "bathrooms", "bedrooms"]
VALID_CITIES = {loc["location_name"].lower().replace("-"," ") for loc in LOCATIONS}

print(VALID_CITIES)

# The main function that cleans the raw data by running helper functions
def clean_data():
    housing_data_db = get_database()
    df = initialize_df(housing_data_db.raw_king_co_listings_data)
    df = handle_missing_values(df)
    df = df.drop_duplicates()
    df = validate_city(df)
    df = standardize_data_types(df)
    df = standardize_string_format(df)
    df = handle_outliers(df)
    df = get_price_per_sqft(df)
    df = categorize_price(df)
    store_data_to_DB(df, housing_data_db.cleaned_king_co_listings_data) 

# Creates dataframe from the raw data in MongoDB
# @param collection is the mongoDB collection where the DF sources data from
def initialize_df(collection):
    try:        
        data = collection.find()
        df = pd.DataFrame(list(data))
        return df
    
    except PyMongoError as e:
        print(f"MongoDB Error: {e}")
    except Exception as e:
        print(f"An Error Occured: {e}")
        
    return pd.DataFrame()

# Filters out non-King County cities from dataframe
def validate_city(df):
    filtered_df = df[df["city"].str.lower().isin(VALID_CITIES)]
    return filtered_df
    
# Handles missing values by filling empty values with appropriate values
def handle_missing_values(df):
    for cols in STRING_COLUMNS:
        df[cols]= df[cols].fillna("")
        
    for cols in NUMERIC_COLUMNS:
        df[cols] = df[cols].replace({"Unknown": np.nan, 0: np.nan, "": np.nan})
    
    df.dropna(subset=["price", "sqft"], how="any", inplace=True)
    return df

# Ensures all columns are the correct datatype
def standardize_data_types(df):
    for col in NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    for col in STRING_COLUMNS:
        df[col] = df[col].astype(str)
        
    df["date"] = pd.to_datetime(df["date"])  
        
    return df

# Ensures all string columns have consistent formatting
def standardize_string_format(df):
    df["city"] = df["city"].str.title().str.strip()
    df["state"] = df["state"].str.upper().str.strip()
    df["zip"] = df["zip"].str.replace(".0","", regex=False)
    return df

# Handles outliers by reducing their statistical impacts using the Winsorize method
# @param group is the data grouped by city
# @param limits is the lower and upper percentiles for outliers
def winsorize_column(group, limits=(0.05, 0.05)):
    return winsorize(group, limits=limits)

# Handles outliers by using the winsorize_column function to transform each city
def handle_outliers(df):
    grouped = df.groupby("city")
    df["price"] = grouped["price"].transform(winsorize_column)
    df["sqft"] = grouped["sqft"].transform(winsorize_column)
    return df

# Adds price_per_sqft column to df
def get_price_per_sqft(df):
    df["price/sqft"] = df["price"] / df["sqft"]
    return df

# Adds price categorizations from low-high based on quantiles of overall king county
def categorize_price(df):
    bins = df['price'].quantile([0, 0.25, 0.5, 0.75, 1.0])
    labels = ["low", "medium_low", "medium_high", "high"]

    df["price_category"] = pd.cut(df["price"], bins=bins, labels=labels, include_lowest=True)
    return df

# Stores data to the cleaned_data collection
def store_data_to_DB(df, collection):
    df_dict = df.to_dict(orient="records")

    try:
        collection.insert_many(df_dict, ordered=False)

        print("Cleaned dataset saved to DB successfully!")
        
    except Exception as e:
        print(f"Data could not be saved to DB: {e}")
        
