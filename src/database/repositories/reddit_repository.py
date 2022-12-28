from src.statistics.sentiments_reddit import sentiments_reddit
import json


class RedditRepository:

    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    def set_values(self):
        psql_delete = """DELETE FROM sentiments_reddit"""
        self.cursor.execute(psql_delete)
        psql = """INSERT into sentiments_reddit(coin_name, coin_symbol, sentiment_value, sentiment_pos, sentiment_neg) VALUES(%s, %s, %s, %s, %s) RETURNING id"""
        # reddit_data = sentiments_reddit()
        reddit_data = sentiments_reddit()
        for reddit in reddit_data:
            # print(reddit['coin_name'], reddit['coin_symbol'], reddit['sentiments_sum'], reddit['sum_pos'], reddit['sum_neg'])
            self.cursor.execute(psql, (str(reddit['coin_name']), str(reddit['coin_symbol']),  float(
                reddit['sentiments_sum']), int(reddit['sum_pos']), int(reddit['sum_neg'])))

            self.conn.commit()
        

    def get_values(self):
        rowarray_list = []
        self.cursor.execute('select * from sentiments_reddit')
        result = self.cursor.fetchall()
        for row in result:
            t = ({"id": row[0],"coin_name": row[1], 'coin_symbol': row[2] ,'sentiment_value': row[3],'sentiment_pos': row[4], 'sentiment_neg': row[5], 'created_at': row[6].strftime("%d-%m-%Y %H:%M:%S")})
            rowarray_list.append(t)

        return json.dumps(rowarray_list)
