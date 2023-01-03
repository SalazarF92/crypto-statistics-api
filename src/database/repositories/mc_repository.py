import json
from src.statistics.monte_carlo import monte_carlo

url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=40&page=1&sparkline=false'


class MCRepository:

    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()

    def monte_carlo_values(self):
        psql = """INSERT into monte_carlo(crypto_exchange, start_date, end_date, next_date, min_variation, max_variation) VALUES(%s, %s, %s, %s, %s, %s) RETURNING id"""
        mc = monte_carlo(url)
        for x in range(len(mc['extreme'])):
            self.cursor.execute(psql, (str(mc['extreme'][x][0]), mc['start'],  mc['end'], mc['next'],
                                float(mc['extreme'][x][1]), float(mc['extreme'][x][2])))
            self.conn.commit()