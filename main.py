from src.database.repositories.cryptos_repository import CryptoRepository
from src.database.repositories.migration import command_tables
from src.database.repositories.reddit_repository import RedditRepository
from src.database.repositories.mc_repository import MCRepository
from postgres import Connection
import time
import schedule


conn = None
url ="https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=40&page=1&sparkline=false"

def main():
    conn = Connection()
    command_tables(conn.conn)

    def job_mc():
        MCRepository(conn.conn).monte_carlo_values()

    def job_sentiment():
        RedditRepository(conn.conn).set_values()
    
    def job_cryptos():
        CryptoRepository(conn.conn, url).set_coins()

    schedule.every(10).seconds.do(job_cryptos)
    # schedule.every(60).seconds.do(job_mc)
    # schedule.every(59).seconds.do(job_sentiment)
    schedule.every().sunday.at("00:30").do(job_cryptos)
    schedule.every().sunday.at("00:30").do(job_mc)
    schedule.every().day.at("06:00").do(job_sentiment)

    def scheduled():
        while True:
            schedule.run_pending()
            time.sleep(1)

    scheduled()


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        exit()
