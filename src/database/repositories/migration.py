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
    CREATE TABLE IF NOT EXISTS cryptos (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        name VARCHAR(255) NOT NULL,
        symbol VARCHAR(255) NOT NULL,
        price VARCHAR(255) NOT NULL,
        market_cap VARCHAR(255) NOT NULL,
        volume_24h VARCHAR(255) NOT NULL,
        percent_change_1h VARCHAR(255) NOT NULL,
        percent_change_24h VARCHAR(255) NOT NULL,
        percent_change_7d VARCHAR(255) NOT NULL,
        last_updated VARCHAR(255) NOT NULL,
        user_id UUID REFERENCES users(id)
    );
"""


# r = requests.get(
#     'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false').json()

# psql = """INSERT INTO coin(name, market_cap, market_cap_rank, symbol, image, max_supply, value) VALUES( % s, % s, % s, % s, % s, % s, % s) RETURNING id"""

# for currency in r:
#     cursor.execute(psql, (currency['name'], currency['market_cap'], currency['market_cap_rank'],
#                           currency['symbol'], currency['image'], currency['max_supply'], currency['current_price']))


def command_tables(conn):
    create_tables = [uuid, monte_carlo, sentiments_reddit]
    for create_table in create_tables:
        conn.cursor().execute(create_table)
        conn.commit()
