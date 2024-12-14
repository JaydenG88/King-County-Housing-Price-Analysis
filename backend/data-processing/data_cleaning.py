import pandas as pd
import numpy as np
from scipy.stats.mstats import winsorize
from database.db_setup import get_database
from pymongo.errors import PyMongoError

STRING_COLUMNS = ["Zip", "Street Address", "State", "URL", "Image", "City"]
NUMERIC_COLUMNS = ["Price", "Square Feet", "Bathrooms", "Bedrooms"]
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
        
    df.dropna(subset=["Price", "Square Feet"], how="any", inplace=True)
    return df

def standardize_data_types(df):
    for col in NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    for col in STRING_COLUMNS:
        df[col] = df[col].astype(str)
    
    return df

def standardize_string_format(df):
    df["City"] = df["City"].str.title().str.strip()
    df["State"] = df["State"].str.upper().str.strip()
    df["Zip"] = df["Zip"].str.replace(".0","", regex=False)

    return df

def winsorize_column(group):
    return winsorize(group, limits=(0.05, 0.05))

def handle_outliers(df):
    grouped = df.groupby("City")
    df["Price"] = grouped["Price"].transform(winsorize_column)
    df["Square Feet"] = grouped["Square Feet"].transform(winsorize_column)
    
    return df

def get_price_per_sqft(df):
    df["Price/Sqft"] = df["Price"] / df["Square Feet"]

    return df

def categorize_price(df):
    bins = df['Price'].quantile([0, 0.25, 0.5, 0.75, 1.0])
    labels = ["Low", "Medium-low", "Medium-High", "High"]

    df["Price Category"] = pd.cut(df["Price"], bins=bins, labels=labels, include_lowest=True)
    return df


def store_data_to_DB(df):
    df_dict = df.to_dict(orient="records")

    try:
        cleaned_king_co_listings_data = HOUSING_DATA_DB.cleaned_king_co_listings_data
        cleaned_king_co_listings_data.insert_many(df_dict)

        print("Cleaned dataset saved to DB successfully!")
        
    except Exception as e:
        print(f"Data could not be saved to DB: {e}")
        
clean_data()