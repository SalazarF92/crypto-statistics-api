from src.database.repositories.migration import command_tables
from src.database.repositories.reddit_repository import RedditRepository
from src.database.repositories.mc_repository import MCRepository
from postgres import Connection
import time
import schedule


conn = None


def main():
    conn = Connection()
    command_tables(conn.conn)

    def job_mc():
        MCRepository(conn.conn).monte_carlo_values()
        
    def job_sentiment():
        RedditRepository(conn.conn).set_values()

    schedule.every(20).seconds.do(job_mc)
    schedule.every(21).seconds.do(job_sentiment)

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
