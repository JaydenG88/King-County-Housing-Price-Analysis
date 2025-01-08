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
from data_ingestion.scraper_config import TARGET_URL, LOCATIONS, USER_AGENTS, ELEMENT_SELECTOR, SCROLL_LIMIT, SCROLL_STEP, SCROLL_TIME

def ingest_data():  
    
    data = []
    for location in LOCATIONS:
        driver = search_location(location["city"],location["code"],location["state"])
        listings_html = extract_listings(driver)
        if len(listings_html) >= 1:
            data += process_listings(listings_html)
        sleep(random.uniform(1,3))
    
    store_data_to_DB(data)
    
def store_data_to_DB(data):
    try:
        housing_data = get_database()
        raw_king_co_listings_data = housing_data.raw_king_co_listings_data
        raw_king_co_listings_data.drop()
        raw_king_co_listings_data.insert_many(data, ordered=False)
        print(f"Successfully uploaded {len(data)} documents to raw_king_co_houses_data")
  
    except Exception as e:
        print(f"Data could not be stored: {e}")
        

def initialize_driver():
    user_agent = random.choice(USER_AGENTS)
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("window-size=1280,1000")
    
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
    return driver

def filter_string(str):
    filtered_string = re.sub(r"[^a-zA-Z0-9 ]", "", str)
    return filtered_string

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
        city = address.split(",")[1].strip()
        return filter_string(city) if city else None
    except Exception as e:
        print(f"Could not retrieve city: {e}")
        return None

def extract_state(listing_soup):
    try:
        state_selector = ELEMENT_SELECTOR["state_selector"]
        address = listing_soup.find(state_selector["elem"], class_=state_selector["selector"]).get_text(strip=True)
        state = address.split(",")[2].split(" ")[1]
        return filter_string(state) if state else None
    except Exception as e:
        print(f"Could not retrieve state: {e}")
        return None

def extract_zip(listing_soup):
    try:
        zip_selector = ELEMENT_SELECTOR["zip_selector"]
        address = listing_soup.find(zip_selector["elem"], class_=zip_selector["selector"]).get_text(strip=True)
        zip = address.split(",")[2].split(" ")[2]
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
    
def scroll_page(driver, scroll_step=SCROLL_STEP):
    max_scrolls = driver.execute_script("return document.body.scrollHeight;") * SCROLL_LIMIT
    current_position = 0
    while current_position < max_scrolls:
        driver.execute_script(f"window.scrollBy(0, {scroll_step});")
        current_position += scroll_step
        sleep(SCROLL_TIME)
                
def search_location(city, code, state):
    try:
        city_url = f"{TARGET_URL}city/{code}/{state}/{city}"
        
        driver = initialize_driver()
        driver.get(city_url)
        print(f"Sucessfully searched: {city}, {state}")
        return driver
    
    except Exception as e:
        print(f"Error: Could not search location: {city}, {state}\nError:{e}")
        driver.quit()
        return None

def extract_listings(driver):
    try: 
        total_listings_selector = ELEMENT_SELECTOR["total_listings_selector"]
        max_pages_selector = ELEMENT_SELECTOR["max_pages_selector"]
        listings_selector = ELEMENT_SELECTOR["listings_selector"]
        homecard_selector = ELEMENT_SELECTOR["homecard_selector"]["selector"]
        button_selector = ELEMENT_SELECTOR["button_selector"]["selector"]
        
        scroll_page(driver)
        sleep(random.uniform(3, 5)) 
        soup = BeautifulSoup(driver.page_source, "html.parser")
        total_listings = int(filter_string(soup.find(total_listings_selector["elem"], class_=total_listings_selector["selector"]).get_text().split(" ")[2]))
        
    except Exception as e:
       print(f"Could not scrape page: {e}")
       driver.quit()
       return []
   
    if total_listings == 0:
        print("No listings found")
        driver.quit()
        return []
   
    max_pages = int(soup.find(max_pages_selector["elem"], attrs={max_pages_selector["attrs"]: max_pages_selector["selector"]}).get_text(strip=True).split()[-1])
    if max_pages == 1:
        try:
            listings_html = soup.find_all(listings_selector["elem"], class_=listings_selector["selector"])
            print(f"Processed page: {max_pages}")
            driver.quit()
            
            print(f"Sucessfully extracted: {len(listings_html)} listings out of {total_listings}")
            return listings_html
        except Exception as e:
            print(f"Unexpected error has occurred: {e}\nOn page: {page_num}")
            driver.quit()
    
    listings_html = []
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
             
            soup = BeautifulSoup(driver.page_source, "html.parser")
        except Exception as e:
            print(f"Unexpected error has occurred: {e}\nOn page: {page_num}")
    
    listings_html += soup.find_all("div", class_="MapHomeCardReact MapHomeCard reversePosition hasBrokerageKeyFacts")
    print(f"Processed page: {max_pages}")
        
    driver.quit()
    print(f"Sucessfully extracted: {len(listings_html)} listings out of {total_listings}")
    return listings_html
        
def process_listings(listings_html):
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
    
