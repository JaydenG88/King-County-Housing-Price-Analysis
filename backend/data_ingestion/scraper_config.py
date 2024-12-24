TARGET_URL = "https://www.redfin.com/"

LOCATIONS =  [
        ["Algona", "WA"], ["Auburn", "WA"], ["Beaux Arts Village", "WA"],
        ["Bellevue", "WA"], ["Black Diamond", "WA"], ["Bothell", "WA"],
        ["Burien", "WA"], ["Carnation", "WA"], ["Clyde Hill", "WA"],
        ["Covington", "WA"], ["Des Moines", "WA"], ["Duvall", "WA"],
        ["Enumclaw", "WA"], ["Federal Way", "WA"], ["Hunts Point", "WA"],
        ["Issaquah", "WA"], ["Kenmore", "WA"], ["Kent", "WA"], 
        ["Kirkland", "WA"], ["Lake Forest Park", "WA"], ["Maple Valley", "WA"],
        ["Medina", "WA"], ["Mercer Island", "WA"], ["Surprise Lake Milton", "WA"],
        ["Newcastle", "WA"], ["Normandy Park", "WA"], ["North Bend", "WA"],
        ["Pacific", "WA"], ["Redmond", "WA"], ["Renton", "WA"],
        ["Sammamish", "WA"], ["SeaTac", "WA"], ["Seattle", "WA"],
        ["Shoreline", "WA"], ["Skykomish", "WA"], ["Snoqualmie", "WA"],
        ["Tukwila", "WA"], ["Woodinville", "WA"], ["Yarrow", "WA"]
    ]

USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    ]

ELEMENT_SELECTOR = {
    "input_selector": {"selector": "search-input-box"},
    "homecard_selector": {"selector": "bp-Homecard"},
    "total_listings_selector": {"elem": "div", "selector": "homes summary reversePosition"},
    "listings_selector": {"elem":"div", "selector": "MapHomeCardReact MapHomeCard reversePosition hasBrokerageKeyFacts"},
    "page_selector": {"elem": "div", "selector": "PhotosView mlsAttributionCardHeight brokerageKeyFactsHeight reversePosition"},
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

SCROLL_LIMIT = 0.75
SCROLL_STEP = 1000
SCROLL_TIME = 0.25
