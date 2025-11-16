COOKIES = {
    "cf_clearance": "A VERY LONG PIECE OF DATA",
    "erfereddde2": "some numbers",
    "gtrgioajorgjap": "some numbers",
    "PHPSESSID": "a mix",
}


BOT_NAME = "opp_scraper"

SPIDER_MODULES = ["scraper"]
NEWSPIDER_MODULE = "scraper"

DOWNLOAD_DELAY = 1.5
RANDOMIZE_DOWNLOAD_DELAY = True

CONCURRENT_REQUESTS = 2
CONCURRENT_REQUESTS_PER_DOMAIN = 2

DEFAULT_REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-US,en;q=0.9",
}

COOKIES_ENABLED = True

ITEM_PIPELINES = {
    "scraper.pipelines.GoogleSheetsPipeline": 300,
}
