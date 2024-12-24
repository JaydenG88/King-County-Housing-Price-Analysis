from data_ingestion.redfin_scraper import get_data
from data_processing.data_cleaning import clean_data
from data_analysis.data_analysis import analyze_data

def main_pipeline():
    get_data()
    clean_data()
    analyze_data()

if __name__ == "__main__":
    main_pipeline()