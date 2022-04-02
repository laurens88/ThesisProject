import sys

import pandas as pd
import requests
import json
from datetime import datetime
import os

bearer_token = "AAAAAAAAAAAAAAAAAAAAAMINZgEAAAAA5x%2Fnm4e%2FYuAaae1N1b7F7czW%2FN8" \
               "%3Dq5K6FTJGdugV5loBhz7iyt2zTgE2nCR4rYUSYoDsdRNZtBgu49"

search_url = 'https://api.twitter.com/2/tweets/search/recent'

# add different query for every label including the additional keywords

#query_params = {'query': 'from:laurens_debruin has:hashtags ', 'tweet.fields': 'text'}


#  Set authorization in request header
def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "laurensThesis"
    return r


#  Create connection between Twitter API and client side
def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


#  Pull tweets from Twitter
def request(limit):
    query_params = {'query': '-has:links -@LinkSync_tech -@cz_binance -#DOJOSWAP (#crypto OR #cryptocurrency OR #BTC OR #ETH OR #altcoin) -giveaway -NFT lang:en -is:retweet', 'max_results': limit}
    json_response = connect_to_endpoint(search_url, query_params)
    filename = "Data/"+datetime.now().strftime("%d-%m-%H-%M")+".json"
    f = open(filename, 'w')
    f.write(json.dumps(json_response, indent=0, sort_keys=True))
    f.close()
    print(f"{query_params['max_results']} tweets pulled.")


#  Merge all json files in Data folder into one json file
def merge():
    directory = "Data"
    ids = []
    tweets = []
    data = []
    datastructure = [{'data': data}]
    duplicate_check = []
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f) and filename != "Tweets.json": #and f is not total file
            current = open(f, 'r')
            values = json.load(current)
            for tweet in range(0, values['meta']['result_count']):
                tweet_id = str(values['data'][tweet]['id'])
                tweet = values['data'][tweet]['text']
                if tweet not in duplicate_check:
                    data.append({'id': tweet_id, 'text': tweet})
                    duplicate_check.append(tweet)
    df = pd.DataFrame(datastructure)
    df.to_json("Data/Tweets.json")
    print(f"{len(duplicate_check)} tweets merged into Tweets.json")

def main():
    request(10)


if __name__ == '__main__':
    main()
