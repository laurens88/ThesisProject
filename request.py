import sys

import pandas as pd
import requests
import json
from datetime import datetime
import os
from difflib import SequenceMatcher

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
    #print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


#  Pull tweets from Twitter
def request(limit):
    query_params = {'query': '-has:links -@LinkSync_tech -@cz_binance -#DOJOSWAP (#crypto OR #cryptocurrency OR #cryptotrading OR #CryptoNews OR #CryptocurrencyNews OR #BTC OR #bitcoin OR #ETH OR #altcoin OR #XRP OR #USDT OR #LUNA OR #Terra OR #ADA OR Cardano OR #BNB OR #AVAX OR #Tether) -betting -giveaway -NFT lang:en -is:retweet', 'max_results': limit}
    json_response = connect_to_endpoint(search_url, query_params)
    filename = "Data/"+datetime.now().strftime("%d-%m-%H-%M")+".json"
    f = open(filename, 'w')
    f.write(json.dumps(json_response, indent=0, sort_keys=True))
    f.close()
    print(f"{query_params['max_results']} tweets pulled.")


#  Merge all json files in Data folder into one json file
def merge():
    directory = "Data"
    data = []
    datastructure = {'data': data}
    duplicate_check = []
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f) and filename != "Tweets.json":
            current = open(f, 'r')
            values = json.load(current)
            for tweet in range(0, values['meta']['result_count']):
                tweet_id = str(values['data'][tweet]['id'])
                tweet = values['data'][tweet]['text']
                if project_block(tweet) and character_spam_check(tweet) and duplicate_checker(tweet, duplicate_check):
                    data.append({'id': tweet_id, 'text': tweet, 'label': "?"})
                    duplicate_check.append(tweet)
                    print(len(data))

    f = open("Data/Tweets.json", 'w')
    f.write(json.dumps(datastructure, indent=0, sort_keys=True))
    f.close()

    print(f"{len(duplicate_check)} tweets merged into Tweets.json")


def duplicate_checker(string, tweet_list):
    for tweet in tweet_list:
        if SequenceMatcher(None, tweet, string).ratio() > 0.9:
            return False
    return True


def character_spam_check(string):
    if "down" in string or "bear" in string:
        return True
    has_counter = 0
    at_counter = 0
    for character in string:
        if character == '#':
            has_counter += 1
        if character == '@':
            at_counter += 1
    if has_counter > 5 or at_counter > 3:
        return False
    return True


def project_block(string):
    if "project" in string:
        return False
    return True


def rank():
    jsonfile = open('Data/Tweets.json', 'r')
    values = json.load(jsonfile)
    jsonfile.close()

    for i in range(len(values['data'])):
        values['data'][i]['rank'] = score_tweet(values['data'][i]['text'])

    #sort descending score
    values['data'] = sorted(values['data'], key=lambda x: x['rank'], reverse=True)

    #delete score key?

    f = open("Data/Tweets.json", 'w')
    f.write(json.dumps(values, indent=0, sort_keys=True))
    f.close()


def score_tweet(string):
    score = 0
    tags = ["#crypto", "#bitcoin", "#btc", "#eth", "#cryptocurrency", "$btc", "$eth", "$xrp", "$sol", "$luna", "$ada",
            "$usdt", "$avax"]
    for tag in tags:
        if tag in string.lower():
            score += 1
    if "$" in string:
        score += 1
    return score


def main():
    request(10)


if __name__ == '__main__':
    main()
