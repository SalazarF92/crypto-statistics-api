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

cryptos =  """
    CREATE TABLE IF NOT EXISTS coin (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        name VARCHAR(255) NOT NULL,
        symbol VARCHAR(255) NOT NULL,
        value VARCHAR(255) NOT NULL,
        market_cap VARCHAR(255) NOT NULL,
        market_cap_rank VARCHAR(255) NOT NULL,
        image VARCHAR(255),
        user_id UUID REFERENCES users(id),
        max_supply VARCHAR(255),
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
"""



def command_tables(conn):
    create_tables = [uuid, monte_carlo, sentiments_reddit, cryptos]
    for create_table in create_tables:
        conn.cursor().execute(create_table)
        conn.commit()
