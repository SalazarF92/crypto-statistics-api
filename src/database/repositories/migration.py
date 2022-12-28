uuid = """
 CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
"""

monte_carlo = """
CREATE TABLE IF NOT EXISTS monte_carlo (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    crypto_exchange VARCHAR(30),
    start_date timestamp,
    end_date timestamp,
    next_date timestamp,
    min_variation float,
    max_variation float,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """


sentiments_reddit = """
                CREATE TABLE IF NOT EXISTS sentiments_reddit(
                    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
                    coin_name VARCHAR(30),
                    coin_symbol VARCHAR(30),
                    sentiment_value float,
                    sentiment_pos int,
                    sentiment_neg int,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )

        """


def command_tables(conn):
    create_tables = [uuid, monte_carlo, sentiments_reddit]
    for create_table in create_tables:
        conn.cursor().execute(create_table)
        conn.commit()
