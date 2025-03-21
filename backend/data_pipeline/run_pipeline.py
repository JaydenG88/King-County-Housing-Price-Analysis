from data_ingestion.scraper import ingest_data
from data_processing.data_cleaning import clean_data
from data_analysis.data_analysis import analyze_data

# Main datapipeline, runs other piplines following an ETL process
def main_pipeline():
    try:
        ingest_data()
    except Exception as e:
        print(f"Failed to extract data: {e}")
    try:
        clean_data()
    except Exception as e:
        print(f"Failed to clean data: {e}")
    try:
        analyze_data()
    except Exception as e:
        print(f"Failed to analyze data: {e}")

if __name__ == "__main__":
    main_pipeline()