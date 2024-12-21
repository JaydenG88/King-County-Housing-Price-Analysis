import pandas as pd
import numpy as np
from scipy.stats.mstats import winsorize
from database.db_setup import get_database
from pymongo.errors import PyMongoError

STRING_COLUMNS = ["zip", "street_address", "state", "URL", "image", "city", "date"]
NUMERIC_COLUMNS = ["price", "sqft", "bathrooms", "bedrooms"]
HOUSING_DATA_DB = get_database()

def clean_data():
    df = initialize_df()
    df = handle_missing_values(df)
    df = df.drop_duplicates()
    df = standardize_data_types(df)
    df = standardize_string_format(df)
    df = handle_outliers(df)
    df = get_price_per_sqft(df)
    df = categorize_price(df)
    store_data_to_DB(df) 
         
def initialize_df():
    try:
        raw_king_co_listings_data = HOUSING_DATA_DB.raw_king_co_listings_data
        
        raw_data = raw_king_co_listings_data.find()
        df = pd.DataFrame(list(raw_data))
        return df
    
    except PyMongoError as e:
        print(f"MongoDB Error: {e}")
    except Exception as e:
        print(f"An Error Occured: {e}")
        
    return pd.DataFrame()

def handle_missing_values(df):
    for cols in STRING_COLUMNS:
        df[cols]= df[cols].fillna("")
        
    for cols in NUMERIC_COLUMNS:
        df[cols] = df[cols].replace({"Unknown": np.nan, 0: np.nan, "": np.nan})
        
    df.dropna(subset=["price", "sqft"], how="any", inplace=True)
    return df

def standardize_data_types(df):
    for col in NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    for col in STRING_COLUMNS:
        df[col] = df[col].astype(str)
    df["date"] = pd.to_datetime(df['date'])  
        
    return df

def standardize_string_format(df):
    df["city"] = df["city"].str.title().str.strip()
    df["state"] = df["state"].str.upper().str.strip()
    df["zip"] = df["zip"].str.replace(".0","", regex=False)
    return df

def winsorize_column(group, limits=(0.05, 0.05)):
    return winsorize(group, limits=limits)

def handle_outliers(df):
    grouped = df.groupby("city")
    df["price"] = grouped["price"].transform(winsorize_column)
    df["sqft"] = grouped["sqft"].transform(winsorize_column)
    return df

def get_price_per_sqft(df):
    df["price/sqft"] = df["price"] / df["sqft"]
    return df

def categorize_price(df):
    bins = df['price'].quantile([0, 0.25, 0.5, 0.75, 1.0])
    labels = ["low", "medium_low", "medium_high", "high"]

    df["price_category"] = pd.cut(df["price"], bins=bins, labels=labels, include_lowest=True)
    return df

def store_data_to_DB(df):
    df_dict = df.to_dict(orient="records")

    try:
        cleaned_king_co_listings_data = HOUSING_DATA_DB.cleaned_king_co_listings_data
        cleaned_king_co_listings_data.insert_many(df_dict, ordered=False)

        print("Cleaned dataset saved to DB successfully!")
        
    except Exception as e:
        print(f"Data could not be saved to DB: {e}")
        
