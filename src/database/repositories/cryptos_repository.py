import requests

url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=40&page=1&sparkline=false"


class CryptoRepository:
    def __init__(self, conn, url):
        self.conn = conn
        self.cursor = conn.cursor()

    def set_coins(self):
        psql_delete = """DELETE FROM coin"""
        self.cursor.execute(psql_delete)

        r = requests.get(url).json()

        psql = """INSERT INTO coin(name, symbol, value, market_cap, market_cap_rank, image, max_supply) VALUES( %s, %s, %s, %s, %s, %s, %s) RETURNING id"""

        for currency in r:
            print(currency)
            self.cursor.execute(
                psql,
                (
                    currency["name"],
                    currency["symbol"],
                    currency["current_price"],
                    currency["market_cap"],
                    currency["market_cap_rank"],
                    currency["image"],
                    currency["max_supply"],
                ),
            )

            self.conn.commit()
