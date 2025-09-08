import os
import sys
import platform
import traceback
from data_ingestion.scraper import ingest_data
from data_processing.data_cleaning import clean_data
from data_analysis.data_analysis import analyze_data

# Disable TensorFlow warnings and configure environment to prevent errors
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Disable TensorFlow logging
os.environ["PYTHONIOENCODING"] = "utf-8"  # Set proper encoding

# Check if running in GitHub Actions
is_github_actions = 'GITHUB_ACTIONS' in os.environ
current_platform = platform.system()

print(f"Running on platform: {current_platform}")
print(f"Running in GitHub Actions: {is_github_actions}")
print(f"Python version: {sys.version}")

# Additional GitHub Actions specific configurations
if is_github_actions:
    # Set environment variables specific to GitHub Actions if needed
    print("Configuring environment for GitHub Actions...")
    # No specific TensorFlow configuration needed for GitHub Actions

# Main datapipeline, runs other piplines following an ETL process
def main_pipeline():
    print("Starting data pipeline...")
    extract_success = False
    clean_success = False
    
    try:
        print("Starting data ingestion process...")
        ingest_data()
        extract_success = True
        print("Data ingestion completed successfully")
    except Exception as e:
        print(f"Failed to extract data: {e}")
        traceback.print_exc()
    
    if extract_success:
        try:
            print("Starting data cleaning process...")
            clean_data()
            clean_success = True
            print("Data cleaning completed successfully")
        except Exception as e:
            print(f"Failed to clean data: {e}")
            traceback.print_exc()
    
    if clean_success:
        try:
            print("Starting data analysis process...")
            analyze_data()
            print("Data analysis completed successfully")
        except Exception as e:
            print(f"Failed to analyze data: {e}")
            traceback.print_exc()
    
    print("Pipeline execution finished")

if __name__ == "__main__":
    main_pipeline()