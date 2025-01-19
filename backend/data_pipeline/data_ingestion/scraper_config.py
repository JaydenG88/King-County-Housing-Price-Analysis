# The main URL of the website being scraped
TARGET_URL = "https://www.redfin.com/"

# Cities that will be searched on Redfin, currently searching King County cities in WA
# Array storing dictionaries containing the city, redfin city ID code, and state
# Path components: https://www.redfin.com/{location_type}/{code}/{state}/{location_name}
# 1. "location_type" - Specific type of location
# 2. "state" - State abbreviation 
# 3. "code" - City identifier (unique numeric ID for the city)
# 4. "location_name" - Name of city
LOCATIONS = [
    {"location_type": "city", "location_name": "Algona", "code": "329", "state": "WA"},
    {"location_type": "city", "location_name": "Auburn", "code": "29438", "state": "WA"},
    {"location_type": "city", "location_name": "Bellevue", "code": "1387", "state": "WA"},
    {"location_type": "city", "location_name": "Black-Diamond", "code": "1672", "state": "WA"},
    {"location_type": "city", "location_name": "Bothell", "code": "29439", "state": "WA"},
    {"location_type": "city", "location_name": "Burien", "code": "2291", "state": "WA"},
    {"location_type": "city", "location_name": "Carnation", "code": "2630", "state": "WA"},
    {"location_type": "city", "location_name": "Clyde-Hill", "code": "3484", "state": "WA"},
    {"location_type": "city", "location_name": "Covington", "code": "3954", "state": "WA"},
    {"location_type": "city", "location_name": "Des-Moines", "code": "5415", "state": "WA"},
    {"location_type": "city", "location_name": "Duvall", "code": "4914", "state": "WA"},
    {"location_type": "city", "location_name": "Enumclaw", "code": "29441", "state": "WA"},
    {"location_type": "city", "location_name": "Federal-Way", "code": "6064", "state": "WA"},
    {"location_type": "city", "location_name": "Hunts-Point", "code": "8371", "state": "WA"},
    {"location_type": "city", "location_name": "Issaquah", "code": "8645", "state": "WA"},
    {"location_type": "city", "location_name": "Kenmore", "code": "8944", "state": "WA"},
    {"location_type": "city", "location_name": "Kent", "code": "9016", "state": "WA"},
    {"location_type": "city", "location_name": "Kirkland", "code": "9148", "state": "WA"},
    {"location_type": "city", "location_name": "Lake-Forest-Park", "code": "9471", "state": "WA"},
    {"location_type": "city", "location_name": "Maple-Valley", "code": "10985", "state": "WA"},
    {"location_type": "city", "location_name": "Medina", "code": "11400", "state": "WA"},
    {"location_type": "city", "location_name": "Mercer-Island", "code": "11460", "state": "WA"},
    {"location_type": "city", "location_name": "Milton", "code": "29442", "state": "WA"},
    {"location_type": "city", "location_name": "Newcastle", "code": "12446", "state": "WA"},
    {"location_type": "city", "location_name": "Normandy-Park", "code": "12667", "state": "WA"},
    {"location_type": "city", "location_name": "North-Bend", "code": "12686", "state": "WA"},
    {"location_type": "city", "location_name": "Pacific", "code": "29443", "state": "WA"},
    {"location_type": "city", "location_name": "Redmond", "code": "14913", "state": "WA"},
    {"location_type": "city", "location_name": "Renton", "code": "14975", "state": "WA"},
    {"location_type": "city", "location_name": "Sammamish", "code": "15735", "state": "WA"},
    {"location_type": "city", "location_name": "SeaTac", "code": "16010", "state": "WA"},
    {"location_type": "city", "location_name": "Seattle", "code": "16163", "state": "WA"},
    {"location_type": "city", "location_name": "Shoreline", "code": "16399", "state": "WA"},
    {"location_type": "city", "location_name": "Skykomish", "code": "16621", "state": "WA"},
    {"location_type": "city", "location_name": "Snoqualmie", "code": "16718", "state": "WA"},
    {"location_type": "city", "location_name": "Tukwila", "code": "18534", "state": "WA"},
    {"location_type": "city", "location_name": "Woodinville", "code": "20001", "state": "WA"},
    {"location_type": "city", "location_name": "Yarrow-point", "code": "20124", "state": "WA"}
]


# User agents which the webscraper cycles through to avoid detection
# Varies in OS, device types, and browsers
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/104.0.1293.63",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
]


# Element Selectors for selenium and beautifulsoup to scrape specific elements
# 1. elem - type of element
# 2. selector - name of element selector
ELEMENT_SELECTOR = {
    "homecard_selector": {"selector": "bp-Homecard"},
    "total_listings_selector": {"elem": "div", "selector": "homes summary reversePosition"},
    "listings_selector": {"elem":"div", "selector": "MapHomeCardReact MapHomeCard reversePosition hasBrokerageKeyFacts"},
    "max_pages_selector": {"elem": "span", "attrs": "data-rf-test-name", "selector": "download-and-save-page-number-text"},
    "button_selector": {"selector": "button[aria-label='next']"},
    "sqft_selector": {"elem":"span", "selector": "bp-Homecard__LockedStat--value"},
    "price_selector": {"elem":"span","selector": "bp-Homecard__Price--value"},
    "street_address_selector": {"elem":"div", "selector": "bp-Homecard__Address flex align-center color-text-primary font-body-xsmall-compact"},
    "city_selector": {"elem": "div", "selector": "bp-Homecard__Address flex align-center color-text-primary font-body-xsmall-compact"},
    "state_selector": {"elem":"div", "selector": "bp-Homecard__Address flex align-center color-text-primary font-body-xsmall-compact"},
    "zip_selector": {"elem":"div", "selector": "bp-Homecard__Address flex align-center color-text-primary font-body-xsmall-compact"},
    "bed_selector": {"elem":"span", "selector": "bp-Homecard__Stats--beds text-nowrap"},
    "bath_selector": {"elem":"span", "selector": "bp-Homecard__Stats--beds text-nowrap"},
    "url_selector": {"elem":"a", "selector": "link-and-anchor visuallyHidden"},
    "img_selector": {"elem":"img", "selector": "bp-Homecard__Photo--image"}
}

# Settings to scroll page
SCROLL_LIMIT = 0.60
SCROLL_STEP = 1000
SCROLL_TIME = 0.25
