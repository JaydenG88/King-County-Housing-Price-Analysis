from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
from time import sleep
from bs4 import BeautifulSoup
import random
import re

TARGET_URL = "https://www.redfin.com/"

def main():
    locations = [
        ["Kent","WA"]
    ]
    data = []
    for location in locations:
        listings_html = find_listings(location[0],location[1])
        data += process_listings(listings_html)
    print(len(data))
    print(data)
        

    
def initialize_driver():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    ]
    user_agent = random.choice(user_agents)
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={user_agent}")


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
    filtered_string = re.sub(r'[^a-zA-Z0-9 ]', '', str)
    return filtered_string

def extract_sqft(listing_soup):
    try:
        sqft = listing_soup.find("span", class_="bp-Homecard__LockedStat--value").get_text(strip=True)
        return filter_string(sqft) if sqft else None
    except Exception as e:
        print(f"Could not retrieve sqft: {e}")
        return None

def extract_price(listing_soup):
    try:
        price = listing_soup.find("span", class_="bp-Homecard__Price--value").get_text(strip=True)
        return filter_string(price) if price else None
    except Exception as e:
        print(f"Could not retrieve price: {e}")
        return None

def extract_street_address(listing_soup):
    try:
        address = listing_soup.find("div", class_="bp-Homecard__Address flex align-center color-text-primary font-body-xsmall-compact").get_text(strip=True)
        street_address = address.split(",")[0]
        return filter_string(street_address) if street_address else None
    except Exception as e:
        print(f"Could not retrieve streed address: {e}")
        return None

def extract_city(listing_soup):
    try:
        address = listing_soup.find("div", class_="bp-Homecard__Address flex align-center color-text-primary font-body-xsmall-compact").get_text(strip=True)
        city = address.split(",")[1].strip()
        return filter_string(city) if city else None
    except Exception as e:
        print(f"Could not retrieve city: {e}")
        return None

def extract_state(listing_soup):
    try:
        address = listing_soup.find("div", class_="bp-Homecard__Address flex align-center color-text-primary font-body-xsmall-compact").get_text(strip=True)
        state = address.split(",")[2].split(" ")[1]
        return filter_string(state) if state else None
    except Exception as e:
        print(f"Could not retrieve state: {e}")
        return None

def extract_zip(listing_soup):
    try:
        address = listing_soup.find("div", class_="bp-Homecard__Address flex align-center color-text-primary font-body-xsmall-compact").get_text(strip=True)
        zip = address.split(",")[2].split(" ")[2]
        return filter_string(zip) if zip else None
    except Exception as e:
        print(f"Could not retrieve zip: {e}")
        return None

def extract_beds(listing_soup):
    try:
        beds = listing_soup.find("span", class_="bp-Homecard__Stats--beds text-nowrap").get_text(strip=True)
        num_beds = beds.split(" ")[0]
        return filter_string(num_beds) if num_beds else None
    except Exception as e:
        print(f"Could not retrieve beds: {e}")
        return None

def extract_baths(listing_soup):
    try:
        baths = listing_soup.find("span", class_="bp-Homecard__Stats--beds text-nowrap").get_text(strip=True)
        num_baths = baths.split(" ")[0]
        return filter_string(num_baths) if num_baths else None
    except Exception as e:
        print(f"Could not retrieve baths: {e}")
        return None
    
def extract_url(listing_soup):
    try:
        url = TARGET_URL + str(listing_soup.find("a", class_="link-and-anchor visuallyHidden")["href"])[1:]
        return url if url else None
    except Exception as e:
        print(f"Could not retrieve url: {e}")
        return None

def extract_img(listing_soup):
    try:
        img = listing_soup.find("img", class_="bp-Homecard__Photo--image")["src"]
        return img if img else None
    except Exception as e:
        print(f"Could not retrieve image: {e}")
        return None
    
def scroll_page(driver, scroll_step=1000):
    max_scrolls = driver.execute_script("return document.body.scrollHeight;") * 0.75
    current_position = 0
    while current_position < max_scrolls:
        driver.execute_script(f"window.scrollBy(0, {scroll_step});")
        current_position += scroll_step
        sleep(0.5)
                

def find_listings(city, state):
    try:
        driver = initialize_driver()
        driver.get(TARGET_URL)
        
        sleep(random.uniform(2, 5))  
        input_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "search-input-box"))
        )
        input_element.send_keys(f"{city} {state}" + Keys.ENTER)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "bp-Homecard"))
        )  
        scroll_page(driver)
        sleep(random.uniform(3, 5)) 

    except Exception as e:
        print(f"Error: Could not process location: {city}, {state}")
        driver.quit()
    
    soup = BeautifulSoup(driver.page_source, "html.parser")
    listings_html = []
    max_pages = int(soup.find("span", attrs={"data-rf-test-name": "download-and-save-page-number-text"}).get_text(strip=True).split()[-1])
    
    for page_num in range(1, max_pages):
        try:            
            listings_html += soup.find_all("div", class_="MapHomeCardReact MapHomeCard reversePosition hasBrokerageKeyFacts")
            print(f"Processed page: {page_num}")
            
            next_page_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='next']"))
            )
            
            next_page_btn.click()
            
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "bp-Homecard"))
            )
            scroll_page(driver)
            sleep(random.uniform(3, 5)) 
            soup = BeautifulSoup(driver.page_source, "html.parser")
            
        except Exception as e:
            print(f"Unexpected error has occurred: {e}\nOn page: {page_num}")
            driver.quit()
    try:
        soup = BeautifulSoup(driver.page_source, "html.parser")       
        listings_html += soup.find_all("div", class_="MapHomeCardReact MapHomeCard reversePosition hasBrokerageKeyFacts")
        print(f"Processed page: {max_pages}")
        
    except Exception as e:
        print(f"Unexpected error has occurred: {e}")
        driver.quit()

    return listings_html

        
def process_listings(listings_html):
    listings_data = []
 
    for listing in listings_html:
        try: 
            listing_soup = BeautifulSoup(str(listing), "html.parser")

            data = {
                "sqft": (sqft := extract_sqft(listing_soup)),
                "price": (price := extract_price(listing_soup)),
                "price/sqft": (float(sqft)/float(price)) if price and sqft else None,
                "zip": extract_zip(listing_soup),
                "city": extract_city(listing_soup),
                "state": extract_state(listing_soup),
                "street_address": extract_street_address(listing_soup),
                "bedrooms": extract_beds(listing_soup),
                "bathrooms": extract_baths(listing_soup),  
                "url": extract_url(listing_soup),
                "img": extract_img(listing_soup)
            }
            listings_data.append(data)
        except Exception as e:
            print(f"Unexpected error has occurred: {e}")

            
    return listings_data

    
if __name__ == "__main__":
    main()
