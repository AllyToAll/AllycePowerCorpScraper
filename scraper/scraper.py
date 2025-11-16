import re
from urllib.parse import urljoin

import scrapy


class CorporationsSpider(scrapy.Spider):
    name = "corporations"
    allowed_domains = ["oppress.games"]

    def __init__(self, name: str | None = None, **kwargs):
        super().__init__(name=name, **kwargs)
        self.current_capital = 0

    def start_requests(self):
        self.COOKIES = self.settings.get("COOKIES")
        url = "https://oppress.games/power/corporations.php?nation=USA"
        yield scrapy.Request(url, cookies=self.COOKIES, callback=self.parse_list_pages)

    def parse_list_pages(self, response):
        page_links = response.css("a.page-link::attr(href)").getall()
        last_page = 1

        for link in page_links:
            if "page=" in link:
                try:
                    page_num = int(link.split("page=")[1].split("&")[0])
                    last_page = max(last_page, page_num)
                except ValueError:
                    continue

        for page in range(1, last_page + 1):
            page_url = f"https://oppress.games/power/corporations.php?page={page}&nation=USA"
            yield scrapy.Request(page_url, cookies=self.COOKIES, callback=self.parse_list)

    def parse_list(self, response):
        capital_text = response.xpath("//text()[contains(., 'CAPITAL')]").get()
        if capital_text:
            match = re.search(r"\$([\d,]+)", capital_text)
            self.current_capital = int(match.group(1).replace(",", "")) if match else 0
        rows = response.css("tr")
        for row in rows:
            shares_info_html = row.css("div.corp-shares-info").get()
            if not shares_info_html:
                continue
            text_raw = " ".join(
                t.strip() for t in
                scrapy.Selector(text=shares_info_html).xpath("//div//text()").getall()
                if t.strip()
            )

            if "shares for sale" not in text_raw:
                continue
            owns_stock = "Your Shares:" in text_raw
            link = row.css("td a::attr(href)").get()
            if link and "corporation.php?corporation=" in link and "details" in link:
                corp_url = urljoin(response.url, link)
                corp_id = link.split("corporation=")[1].split("&")[0]

                yield scrapy.Request(
                    corp_url,
                    cookies=self.COOKIES,
                    callback=self.parse_details,
                    meta={
                        "corp_id": corp_id,
                        "_owns_stock": owns_stock,
                    }
                )

    def parse_details(self, response):
        corp_id = response.meta["corp_id"]
        owns_stock = response.meta["_owns_stock"]

        corp_name = response.css("h1.corp-name-title::text").get()
        corp_name = corp_name.strip() if corp_name else "Unknown"

        dividends_text = response.xpath(
            "//td[text()='Dividends']/following-sibling::td/text()"
        ).get()
        if dividends_text:
            match = re.search(r"\b\d+%|\d+\.\d+%", dividends_text)
            dividends_percent = match.group(0) if match else "0%"
        else:
            dividends_percent = "0%"

        income = response.xpath(
            "//td[text()='Income']/following-sibling::td/text()"
        ).get()
        income = income.replace("$", "").replace(",", "").strip() if income else "0"

        stock_url = f"https://oppress.games/power/corporation.php?corporation={corp_id}&stockdetails"
        yield scrapy.Request(
            stock_url,
            cookies=self.COOKIES,
            callback=self.parse_stock,
            meta={
                "corp_name": corp_name,
                "dividends_percent": dividends_percent,
                "income": income,
                "_owns_stock": owns_stock,
            },
        )

    def parse_stock(self, response):
        corp_name = response.meta["corp_name"]
        dividends_percent = response.meta["dividends_percent"]
        income = response.meta["income"]
        owns_stock = response.meta["_owns_stock"]

        def extract(label):
            return response.xpath(
                f"//span[text()='{label}']/following-sibling::span/text()"
            ).get()

        current_price = extract("Current Stock Price:")
        current_price = current_price.replace("$", "").replace(",", "") if current_price else "0"

        total_shares = extract("Total Shares:")
        total_shares = total_shares.replace(",", "") if total_shares else "0"

        lowest_ask = response.css("span.price-green::text").get()
        lowest_ask = lowest_ask.replace("$", "").replace(",", "") if lowest_ask else "0"

        shares_owned = response.xpath("//input[@id[contains(., 'sell_share_')]]/@max").get()
        shares_owned = shares_owned.strip() if shares_owned else "0"
        yield {
            "corp_name": corp_name,
            "shares_owned": shares_owned,
            "current_price": current_price,
            "lowest_ask": lowest_ask,
            "total_shares": total_shares,
            "income": income,
            "dividends": dividends_percent,
            "_owns_stock": owns_stock,
        }
