from cmath import isnan
import pandas as pd
import numpy as np

# misc
# import datetime as dt
# from pprint import pprint
# from itertools import chain

# from sqlalchemy import null
# reddit crawler
import praw
import requests

# sentiment analysis
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# from nltk.tokenize import word_tokenize, RegexpTokenizer # tokenize words
# from nltk.corpus import stopwords

# import nltk

nltk.download("vader_lexicon")  # get lexicons data
# nltk.download('punkt') # for tokenizer
# nltk.download('stopwords')

url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=40&page=1&sparkline=false"

coins = requests.get(url).json()

r = praw.Reddit(
    user_agent="salazares",
    client_id="CyPDUtS0eI9oe3uMUthV5A",
    client_secret="YJWKfOiJKzVKkXZ90bnbLgjcpT_e6g",
    check_for_async=False,
)


def sentiments_reddit():
    print('startei sentiments')

    all_coins_subreddit = []
    all_data = []

    for i in range(len(coins)):

        try:
            subreddit_01 = r.subreddit(coins[i]["symbol"])
            # top posts all time
            crypto_currencies = [*subreddit_01.top(limit=70)]
            all_coins_subreddit.append(
                [coins[i]["name"], coins[i]["symbol"], crypto_currencies]
            )
        except:
            pass

    for news in all_coins_subreddit:
    
        title = [news[2].title for news[2] in news[2]]

        news_coin = pd.DataFrame({"title": title})

        sid = SentimentIntensityAnalyzer()
        res = [*news_coin["title"].apply(sid.polarity_scores)]
        # pprint(res[:3])

        sentiment_df = pd.DataFrame.from_records(res)
        result_compound = pd.concat([news_coin, sentiment_df], axis=1, join="inner")

        THRESHOLD = 0.2

        conditions = [
            (result_compound["compound"] <= -THRESHOLD),
            (result_compound["compound"] > -THRESHOLD)
            & (result_compound["compound"] < THRESHOLD),
            (result_compound["compound"] >= THRESHOLD),
        ]

        values = ["neg", "neu", "pos"]

        result_compound["label"] = np.select(conditions, values)

        print(
            news[0],
            news[1],
            result_compound.pos[result_compound.pos != 0].mean(),
            result_compound.neg[result_compound.neg != 0].mean(),
        )

        sum_pos = 0
        exists_pos = "pos" in result_compound["label"].value_counts()
        if exists_pos:
            sum_pos = result_compound["label"].value_counts().pos

        sum_neg = 0
        exists_neg = "neg" in result_compound["label"].value_counts()
        if exists_neg:
            sum_neg = result_compound["label"].value_counts().neg

        if isnan(
            result_compound.pos[result_compound.pos != 0].mean()
            - result_compound.neg[result_compound.neg != 0].mean()
        ):
            continue

        else:
            all_data.append(
                {
                    "coin_name": news[0],
                    "coin_symbol": news[1],
                    "sentiments_sum": format(
                        result_compound.pos[result_compound.pos != 0].mean()
                        - result_compound.neg[result_compound.neg != 0].mean(),
                        ".4f",
                    ),
                    "sum_pos": sum_pos,
                    "sum_neg": sum_neg,
                }
            )

    return all_data
