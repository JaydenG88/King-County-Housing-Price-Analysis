TARGET_URL = "https://www.redfin.com/"

LOCATIONS = [
    {"city": "Algona", "code": "329", "state": "WA"},
    {"city": "Auburn", "code": "29438", "state": "WA"},
    {"city": "Bellevue", "code": "1387", "state": "WA"},
    {"city": "Black-Diamond", "code": "1672", "state": "WA"},
    {"city": "Bothell", "code": "29439", "state": "WA"},
    {"city": "Burien", "code": "2291", "state": "WA"},
    {"city": "Carnation", "code": "2630", "state": "WA"},
    {"city": "Clyde-Hill", "code": "3484", "state": "WA"},
    {"city": "Covington", "code": "3954", "state": "WA"},
    {"city": "Des-Moines", "code": "5415", "state": "WA"},
    {"city": "Duvall", "code": "4914", "state": "WA"},
    {"city": "Enumclaw", "code": "29441", "state": "WA"},
    {"city": "Federal-Way", "code": "6064", "state": "WA"},
    {"city": "Hunts-Point", "code": "8371", "state": "WA"},
    {"city": "Issaquah", "code": "8645", "state": "WA"},
    {"city": "Kenmore", "code": "8944", "state": "WA"},
    {"city": "Kent", "code": "9016", "state": "WA"},
    {"city": "Kirkland", "code": "9148", "state": "WA"},
    {"city": "Lake-Forest-Park", "code": "9471", "state": "WA"},
    {"city": "Maple-Valley", "code": "10985", "state": "WA"},
    {"city": "Medina", "code": "11400", "state": "WA"},
    {"city": "Mercer-Island", "code": "11460", "state": "WA"},
    {"city": "Milton", "code": "29442", "state": "WA"},
    {"city": "Newcastle", "code": "12446", "state": "WA"},
    {"city": "Normandy-Park", "code": "12667", "state": "WA"},
    {"city": "North-Bend", "code": "12686", "state": "WA"},
    {"city": "Pacific", "code": "29443", "state": "WA"},
    {"city": "Redmond", "code": "14913", "state": "WA"},
    {"city": "Renton", "code": "14975", "state": "WA"},
    {"city": "Sammamish", "code": "15735", "state": "WA"},
    {"city": "SeaTac", "code": "16010", "state": "WA"},
    {"city": "Seattle", "code": "16163", "state": "WA"},
    {"city": "Shoreline", "code": "16399", "state": "WA"},
    {"city": "Skykomish", "code": "16621", "state": "WA"},
    {"city": "Snoqualmie", "code": "16718", "state": "WA"},
    {"city": "Tukwila", "code": "18534", "state": "WA"},
    {"city": "Woodinville", "code": "20001", "state": "WA"},
    {"city": "Yarrow-point", "code": "20124", "state": "WA"}
]

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

SCROLL_LIMIT = 0.60
SCROLL_STEP = 1000
SCROLL_TIME = 0.25
