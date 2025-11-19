import gspread
from google.oauth2.service_account import Credentials


def clear_extra_rows(sheet, next_row, max_row):
    if next_row <= max_row:
        clear_range = f"A{next_row}:G{max_row}"
        sheet.batch_clear([clear_range])


class GoogleSheetsPipeline:

    def open_spider(self, spider):
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]

        creds = Credentials.from_service_account_file(
            "credentials.json",
            scopes=scopes
        )
        client = gspread.authorize(creds)

        self.sheet1 = client.open("Power").worksheet("Prices")
        self.sheet2 = client.open("Power").worksheet("Income")

        self.row1 = 2
        self.row2 = 2

    def process_item(self, item, spider):
        shares_owned = int(item["shares_owned"]) if item["shares_owned"] else 0
        current_price = float(item["current_price"]) if item["current_price"] else 0.0
        lowest_ask = float(item["lowest_ask"]) if item["lowest_ask"] else 0.0
        total_shares = int(item["total_shares"]) if item["total_shares"] else 0
        income = float(item["income"]) if item["income"] else 0.0
        dividends = int(item["dividends"].replace("%", "")) / 100 if item["dividends"] else 0

        row_values = [
            item["corp_name"],
            shares_owned,
            current_price,
            lowest_ask,
            total_shares,
            income,
            dividends,
        ]
        self.sheet1.update(f"A{self.row1}:G{self.row1}", [row_values])
        self.row1 += 1
        owns_stock = item.get("_owns_stock", False)
        if owns_stock:
            self.sheet2.update(f"A{self.row2}:G{self.row2}", [row_values])
            self.row2 += 1

        return item

    def close_spider(self, spider):
        if hasattr(spider, "current_capital"):
            self.sheet1.update("P2", [[spider.current_capital]])
            self.sheet2.update("P2", [[spider.current_capital]])
        clear_extra_rows(self.sheet1, self.row1, 100)
        clear_extra_rows(self.sheet2, self.row2, 100)
