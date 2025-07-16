from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
from time import sleep
from bs4 import BeautifulSoup
from datetime import date
from database.db_setup import get_database
import random
import re
import shutil
import tempfile
from data_ingestion.scraper_config import TARGET_URL, LOCATIONS, USER_AGENTS, ELEMENT_SELECTOR, SCROLL_LIMIT, SCROLL_STEP, SCROLL_TIME, SEARCH_FILTER

# Main function that runs the data extraction process
# Searches locations and extracts data using a web scraper and web driver
# Stores data to a Mongodb database
def ingest_data():  
    # stores the extracted and processed listings
    data = []
    
    # Iterates through locations to scrape and process listings
    for location in LOCATIONS:
        driver, temp_profile = search_location(location)
        listings_html = extract_listings(driver, temp_profile)
        
        if len(listings_html) >= 1:
            data += process_listings(listings_html)
        # Sleep to delay and not overload site requests
        sleep(random.uniform(1,3))
    
    store_data_to_DB(data)

# Stores array of objects/dictionaries into Mongo database
# @param data is the data being stored into the database
def store_data_to_DB(data):
    try:
        # Initializes database and collection reference
        housing_data = get_database()
        raw_king_co_listings_data = housing_data.raw_king_co_listings_data
        
        # Drops old existing raw data (uncleaned data won't be used in analysis) and inserts new raw data
        raw_king_co_listings_data.drop()
        raw_king_co_listings_data.insert_many(data, ordered=False)
        print(f"Successfully uploaded {len(data)} documents to raw_king_co_houses_data")
  
    except Exception as e:
        print(f"Data could not be stored: {e}")
        
# Initializes selenium webdriver to scrape dynamically loaded pages
def initialize_driver():
    try:
        user_agent = random.choice(USER_AGENTS)
        temp_profile = tempfile.mkdtemp()  

        options = webdriver.ChromeOptions()
        options.add_argument(f"user-agent={user_agent}")
        options.add_argument("window-size=1280,1000")
        options.add_argument(f"--user-data-dir={temp_profile}")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--headless")

        driver = webdriver.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )
        return driver, temp_profile
    except Exception as e:
        print(f"Error initializing driver: {e}")
        if 'temp_profile' in locals():
            shutil.rmtree(temp_profile)
        return None, None


# Filters out non-alphanumeric characters and returns cleaned string
# @param str is the string being filtered
def filter_string(str):
    filtered_string = re.sub(r"[^a-zA-Z0-9 ]", "", str)
    return filtered_string

# The extract functions finds and returns the specific element and value of the data category needed
# Data categories are: sqft, price, street address, city, state, zip, beds, baths, url, and img
# @param listing_soup is the beautiful soup html parser
def extract_sqft(listing_soup):
    try:
        sqft_selector = ELEMENT_SELECTOR["sqft_selector"]
        sqft = listing_soup.find(sqft_selector["elem"], class_=sqft_selector["selector"]).get_text(strip=True)
        return filter_string(sqft) if sqft else None
    except Exception as e:
        print(f"Could not retrieve sqft: {e}")
        return None

def extract_price(listing_soup):
    try:
        price_selector = ELEMENT_SELECTOR["price_selector"]
        price = listing_soup.find(price_selector["elem"], class_=price_selector["selector"]).get_text(strip=True)
        return filter_string(price) if price else None
    except Exception as e:
        print(f"Could not retrieve price: {e}")
        return None

def extract_street_address(listing_soup):
    try:
        street_address_selector = ELEMENT_SELECTOR["street_address_selector"]
        address = listing_soup.find(street_address_selector["elem"], class_=street_address_selector["selector"]).get_text(strip=True)
        street_address = address.split(",")[0]
        return filter_string(street_address) if street_address else None
    except Exception as e:
        print(f"Could not retrieve streed address: {e}")
        return None

def extract_city(listing_soup):
    try:
        city_selector = ELEMENT_SELECTOR["city_selector"]
        address = listing_soup.find(city_selector["elem"], class_=city_selector["selector"]).get_text(strip=True)
        address_arr = address.split(",")

        city = address_arr[len(address_arr)-2].strip()
        return filter_string(city) if city else None
    except Exception as e:
        print(f"Could not retrieve city: {e}")
        return None

def extract_state(listing_soup):
    try:
        state_selector = ELEMENT_SELECTOR["state_selector"]
        address = listing_soup.find(state_selector["elem"], class_=state_selector["selector"]).get_text(strip=True)
        address_arr = address.split(",")
        
        state = address_arr[len(address_arr)-1].split(" ")[1]
        return filter_string(state) if state else None
    except Exception as e:
        print(f"Could not retrieve state: {e}")
        return None

def extract_zip(listing_soup):
    try:
        zip_selector = ELEMENT_SELECTOR["zip_selector"]
        address = listing_soup.find(zip_selector["elem"], class_=zip_selector["selector"]).get_text(strip=True)
        address_arr = address.split(",")
        
        zip = address_arr[len(address_arr)-1].split(" ")[2]
        return filter_string(zip) if zip else None
    except Exception as e:
        print(f"Could not retrieve zip: {e}")
        return None

def extract_beds(listing_soup):
    try:
        bed_selector = ELEMENT_SELECTOR["bed_selector"]
        beds = listing_soup.find(bed_selector["elem"], class_=bed_selector["selector"]).get_text(strip=True)
        num_beds = beds.split(" ")[0]
        return filter_string(num_beds) if num_beds else None
    except Exception as e:
        print(f"Could not retrieve beds: {e}")
        return None

def extract_baths(listing_soup):
    try:
        bath_selector = ELEMENT_SELECTOR["bath_selector"]
        baths = listing_soup.find(bath_selector["elem"], class_=bath_selector["selector"]).get_text(strip=True)
        num_baths = baths.split(" ")[0]
        return filter_string(num_baths) if num_baths else None
    except Exception as e:
        print(f"Could not retrieve baths: {e}")
        return None
    
def extract_url(listing_soup):
    try:
        url_selector = ELEMENT_SELECTOR["url_selector"]
        url = TARGET_URL + str(listing_soup.find(url_selector["elem"], class_=url_selector["selector"])["href"])[1:]
        return url if url else None
    except Exception as e:
        print(f"Could not retrieve url: {e}")
        return None

def extract_img(listing_soup):
    try:
        img_selector = ELEMENT_SELECTOR["img_selector"]
        img = listing_soup.find(img_selector["elem"], class_=img_selector["selector"])["src"]
        return img if img else None
    except Exception as e:
        print(f"Could not retrieve image: {e}")
        return None

# Makes webdriver scroll through pages to render javascript and avoiding bot detection
# @param driver is the selenium webdriver
# @param scroll_step is the scroll interval
# @param scroll_limit is the percentage of the page that will be scrolled to (in decimal format, 1.0 = 100%, 0.5 = 50%) 
def scroll_page(driver, scroll_step=SCROLL_STEP, scroll_limit=SCROLL_LIMIT):
    max_scrolls = driver.execute_script("return document.body.scrollHeight;") * scroll_limit
    current_position = 0
    # Scrolls until scroll limit is met
    while current_position < max_scrolls:
        driver.execute_script(f"window.scrollBy(0, {scroll_step});")
        current_position += scroll_step
        sleep(SCROLL_TIME)
        
# Searches specified location on redfin through the selenium webdriver and returns webdriver
# @param location is the location being searched    
def search_location(location):
    location_type = location["location_type"]
    location_name = location["location_name"]
    code = location["code"]
    state = location["state"]

    try:
        city_url = f"{TARGET_URL}{location_type}/{code}/{state}/{location_name}/{SEARCH_FILTER}"
        driver, temp_profile = initialize_driver()
        driver.get(city_url)
        print(f"Successfully searched: {location_name}, {state}")
        return driver, temp_profile
    except Exception as e:
        print(f"Error: Could not search location: {location_name}, {state}\nError: {e}")
        driver.quit()
        shutil.rmtree(temp_profile)
        return None, None

# Extracts and returns the raw HTML of each listing from each page of the searched location
# @param driver is the webdriver containing the searched location on redfin
def extract_listings(driver, temp_profile):
    try: 
        total_listings_selector = ELEMENT_SELECTOR["total_listings_selector"]
        max_pages_selector = ELEMENT_SELECTOR["max_pages_selector"]
        listings_selector = ELEMENT_SELECTOR["listings_selector"]
        homecard_selector = ELEMENT_SELECTOR["homecard_selector"]["selector"]
        button_selector = ELEMENT_SELECTOR["button_selector"]["selector"]
        
        # Scrolls first page and sleeps to render the first page (also helps avoids bot detection)
        scroll_page(driver)
        sleep(random.uniform(3, 5)) 
        # Parses the html of the first page and finds total amount of listings
        soup = BeautifulSoup(driver.page_source, "html.parser")
        total_listings = int(filter_string(soup.find(total_listings_selector["elem"], class_=total_listings_selector["selector"]).get_text().split(" ")[0]))

    except Exception as e:
       print(f"Could not scrape page: {e}")
       driver.quit()
       shutil.rmtree(temp_profile)
       return []
   
   # Skips location and returns an empty array if there are no listings 
    if total_listings == 0:
        print("No listings found")
        driver.quit()
        shutil.rmtree(temp_profile)
        return []
   
   # Finds max pages to know if pages should be progressed through
    max_pages = int(soup.find(max_pages_selector["elem"], attrs={max_pages_selector["attrs"]: max_pages_selector["selector"]}).get_text(strip=True).split()[-1])
    # Scrapes and returns contents of the first page if there is only one page
    if max_pages == 1:
        try:
            listings_html = soup.find_all(listings_selector["elem"], class_=listings_selector["selector"])

            print(f"Processed page: {max_pages}")
            driver.quit()
            shutil.rmtree(temp_profile)

            
            print(f"Sucessfully extracted: {len(listings_html)} listings out of {total_listings}")
            return listings_html
        except Exception as e:
            print(f"Unexpected error has occurred: {e}\nOn page: {page_num}")
            driver.quit()
            shutil.rmtree(temp_profile)

    
    listings_html = []
    # Iterates through each page and scrapes the HTML of each listing
    for page_num in range(1, max_pages):
        try:            
            listings_html += soup.find_all(listings_selector["elem"], class_=listings_selector["selector"])
            print(f"Processed page: {page_num}")
            
            next_page_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, button_selector))
            )

            next_page_btn.click()
            
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, homecard_selector))
            )
            
            scroll_page(driver)
             
             # Scrapes the HTML of the webdriver's page
            soup = BeautifulSoup(driver.page_source, "html.parser")
        except Exception as e:
            print(f"Unexpected error has occurred: {e}\nOn page: {page_num}")
    
    # Scrapes final page of the searched location
    listings_html += soup.find_all("div", class_="MapHomeCardReact MapHomeCard reversePosition hasBrokerageKeyFacts")
    print(f"Processed page: {max_pages}")
        
    driver.quit()
    shutil.rmtree(temp_profile)
    print(f"Sucessfully extracted: {len(listings_html)} listings out of {total_listings}")
    return listings_html

# Processes the raw HTML of each listing into usable data separated into categories
# @param listings_html is the raw html of the housing listings     
def process_listings(listings_html):
    # Stores all the processed listings
    listings_data = []
    processed_count = 0

    for listing in listings_html:
        try: 
            listing_soup = BeautifulSoup(str(listing), "html.parser")
            
            data = {
                "sqft": (extract_sqft(listing_soup)),
                "price": (extract_price(listing_soup)),
                "zip": extract_zip(listing_soup),
                "city": extract_city(listing_soup),
                "state": extract_state(listing_soup),
                "street_address": extract_street_address(listing_soup),
                "bedrooms": extract_beds(listing_soup),
                "bathrooms": extract_baths(listing_soup),  
                "URL": (URL := extract_url(listing_soup)),
                "image": extract_img(listing_soup),
                "date": str(date.today()),
                "_id": URL
            }

            listings_data.append(data)
            processed_count += 1
            
        except Exception as e:
            print(f"Unexpected error has occurred: {e}")
            
    print(f"Sucessfully processed: {processed_count} out of {len(listings_html)}")
    return listings_data

