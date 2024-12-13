import pandas as pd
import numpy as np
from scipy.stats.mstats import winsorize
from database.db_setup import get_database

try:
    housing_data = get_database()
    
    raw_king_co_listings_data = housing_data.raw_king_co_listings_data
    
    raw_data = raw_king_co_listings_data.find()
    print(raw_data)
    df = pd.DataFrame(list(raw_data))

except Exception as e:
    print(f"An Error Occured: {e}")
    
print("Initial Data Sample:\n")
print(df.head())

print("\nDataset Overview:\n")
print(df.info())

print("\nDescriptive Statistics:\n")
print(df.describe())

print("\nChecking for Missing Values:\n")
print(df.isnull().sum())

string_columns = ["Zip", "Street Address", "State", "URL", "Image", "City"]
for cols in string_columns:
    df[cols]= df[cols].fillna("")
    
numeric_columns = ["Price", "Square Feet", "Bathrooms", "Bedrooms"]
for cols in numeric_columns:
    df[cols] = df[cols].replace({"Unknown": np.nan, 0: np.nan, "": np.nan})

df = df.dropna(subset=["Price", "Square Feet"], how="any")
df = df.drop_duplicates()

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

for col in string_columns:
    df[col] = df[col].astype(str)
    
df["City"] = df["City"].str.title().str.strip()
df["State"] = df["State"].str.upper().str.strip()
df["Zip"] = df["Zip"].str.replace(".0","", regex=False)

grouped = df.groupby("City")
Q1 = grouped["Price"].transform(lambda x: x.quantile(0.25))
Q3 = grouped["Price"].transform(lambda x: x.quantile(0.75))
IQR = Q3 - Q1

lower_lim = Q1 - 1.5 * IQR
upper_lim = Q3 + 1.5 * IQR

df["Is_Outlier"] = (df["Price"] < lower_lim) | (df["Price"] > upper_lim)
print(df[df["Is_Outlier"]])

def winsorize_column(group):
    return winsorize(group, limits=(0.05, 0.05))

df["Price"] = grouped["Price"].transform(winsorize_column)
df["Square Feet"] = grouped["Square Feet"].transform(winsorize_column)

df["Price/Sqft"] = df["Price"] / df["Square Feet"]

bins = df['Price'].quantile([0, 0.25, 0.5, 0.75, 1.0])
labels = ["Low", "Medium-low", "Medium-High", "High"]

df["Price Category"] = pd.cut(df["Price"], bins=bins, labels=labels, include_lowest=True)

df = df.drop(columns=["Is_Outlier"])

print("\nFinal Dataset Overview:")
print(df.info())

print("\nFinal Descriptive Statistics:")
print(df.describe())

print("\nUnique Values in Categorical Columns:")
for col in ['City', 'State', 'Price Category']:
    print(f"\n{col} unique values:")
    print(df[col].value_counts())
    
print("\nRemaining Missing Values:")
print(df.isnull().sum())

df_dict = df.to_dict(orient="records")
try:
    cleaned_king_co_listings_data = housing_data.cleaned_king_co_listings_data
    cleaned_king_co_listings_data.insert_many(df_dict)

    print("Cleaned dataset saved to DB successfully!")
    
except Exception as e:
    print(f"Data could not be saved to DB: {e}")