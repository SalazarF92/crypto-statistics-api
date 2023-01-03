import os
import psycopg2


class Connection:
    def __init__(self):
        self.conn = None

        try:
            self.conn = psycopg2.connect(
                user=os.getenv("PGUSER"),
                password=os.getenv("PGPASSWORD"),
                host=os.getenv("PGHOST"),
                port=os.getenv("PGPORT"),
                database=os.getenv("PGDATABASE"),
            )
            self.cursor = self.conn.cursor()

            print("PostgreSQL server information")
            print(self.conn.get_dsn_parameters(), "\n")
            self.cursor.execute("SELECT version();")
            record = self.cursor.fetchone()
            print("You are connected to - ", record)
        except:
            print("Error while connecting to PostgreSQL")
