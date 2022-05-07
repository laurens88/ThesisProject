import requests
import json
from datetime import datetime
import os
from difflib import SequenceMatcher
from sklearn.model_selection import train_test_split

bearer_token = "AAAAAAAAAAAAAAAAAAAAAMINZgEAAAAA5x%2Fnm4e%2FYuAaae1N1b7F7czW%2FN8" \
               "%3Dq5K6FTJGdugV5loBhz7iyt2zTgE2nCR4rYUSYoDsdRNZtBgu49"

search_url = 'https://api.twitter.com/2/tweets/search/recent'


#  Set authorization in request header
def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "laurensThesis"
    return r


#  Create connection between Twitter API and client side
def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


#  Pull tweets from Twitter with general query
def request(limit):
    query_params = {'query': '-project (#BTC OR #bitcoin OR #cardano OR #XRP OR #ETH) -Airdrop -#Airdrop -betting '
                             '-giveaway -NFT lang:en -is:retweet', 'max_results': limit}
    json_response = connect_to_endpoint(search_url, query_params)
    filename = "Data/"+datetime.now().strftime("%d-%m-%H-%M")+".json"
    f = open(filename, 'w')
    f.write(json.dumps(json_response, indent=0, sort_keys=True))
    f.close()
    print(f"{query_params['max_results']} tweets pulled.")


#  Pull tweets from Twitter with query for tweets with media
def request_media(limit):
    query_params = {'query': 'has:media -project (#BTC OR #bitcoin OR #cardano OR #XRP OR #ETH) '
                             '-Airdrop -#Airdrop -betting -giveaway -NFT lang:en -is:retweet', 'max_results': limit}
    json_response = connect_to_endpoint(search_url, query_params)
    filename = "Data/"+datetime.now().strftime("%d-%m-%H-%M")+".json"
    f = open(filename, 'w')
    f.write(json.dumps(json_response, indent=0, sort_keys=True))
    f.close()
    print(f"{query_params['max_results']} media tweets pulled.")


#  Pull tweets from Twitter with query for negative sentiment tweets
def request_neg(limit):
    query_params = {'query': '-project (#BTC OR #bitcoin OR #cardano OR #XRP OR #ETH) '
                             '(down OR bear OR bearish OR unstable OR weak OR crash OR down by OR 📉 OR scam OR 💸 '
                             'OR desperate OR lost OR risky OR sad OR decreasing) -Airdrop -#Airdrop -betting -giveaway'
                             '-NFT lang:en -is:retweet', 'max_results': limit}
    json_response = connect_to_endpoint(search_url, query_params)
    filename = "Data/"+datetime.now().strftime("%d-%m-%H-%M")+".json"
    f = open(filename, 'w')
    f.write(json.dumps(json_response, indent=0, sort_keys=True))
    f.close()
    print(f"{query_params['max_results']} negative tweets pulled.")


#  Merge all json files in Data folder into one json file called 'Tweets.json'
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

    path, dirs, files = next(os.walk("Backups"))
    file_count = len(files)
    filename = f"Backups/Tweets{file_count}.json"

    f = open(filename, 'w')
    f.write(json.dumps(datastructure, indent=0, sort_keys=True))
    f.close()

    print(f"{len(duplicate_check)} tweets merged into Tweets.json")


# Block tweets that match more than 90% to tweets that are already included.
def duplicate_checker(string, tweet_list):
    for tweet in tweet_list:
        if SequenceMatcher(None, tweet, string).ratio() > 0.9:
            return False
    return True


# Block tweets containing excess amount of # or @ for Tweets.json merge.
def character_spam_check(string):
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


# Block tweets containing the word 'project' for Tweets.json merge
def project_block(string):
    if "project" in string:
        return False
    return True


# Compute and insert rank values for tweets in Tweets.json
def rank():
    jsonfile = open('Data/Tweets.json', 'r')
    values = json.load(jsonfile)
    jsonfile.close()

    for i in range(len(values['data'])):
        values['data'][i]['rank'] = score_tweet(values['data'][i]['text'])

    # sort descending score
    values['data'] = sorted(values['data'], key=lambda x: x['rank'], reverse=True)

    f = open("Data/Tweets.json", 'w')
    f.write(json.dumps(values, indent=0, sort_keys=True))
    f.close()

    print("Tweets.json is now ranked")


# Return the score for tweet that is passed as parameter 'string'
def score_tweet(string):
    score = 0
    tags = ["bitcoin", "cardano", "ethereum", "ripple", "avax", "avalanche", "#crypto", "#bitcoin", "#btc",
            "#eth", "#xrp", "#cryptocurrency", "#altcoin", "$btc", "$eth", "$xrp", "$sol", "$luna", "$ada",
            "$usdt", "$avax"]
    unrelated = [" nft ", "giveaway", "airdrop", "lightning", "#coinhuntworld", "#MasterMetals", "down", "up",
                 "bear", "bull", "long", "short", "change", "fear", "%"]
    for tag in tags:
        if tag in string.lower():
            score += 1
    for token in unrelated:
        if token in string.lower():
            score -= 5
    if "$" in string:
        score += 1
    if "%" in string:
        score += 1
    return score


# Print the distribution of ranks in Tweets.json
def rank_distribution():
    jsonfile = open('Data/Tweets.json', 'r')
    values = json.load(jsonfile)
    jsonfile.close()

    distribution = {}

    for i in range(len(values['data'])):
        tweet_rank = str(values['data'][i]['rank'])
        if tweet_rank in distribution.keys():
            distribution[tweet_rank] += 1
        else:
            distribution[tweet_rank] = 1

    ranks = sorted(distribution.keys(), key=lambda x: int(x))
    rank_index = 0
    while len(distribution.keys()) > 0:
        print(f"Rank {ranks[rank_index]} occurs "
              f"{distribution.pop(str(min([int(x) for x in distribution.keys()])))} times.")
        rank_index += 1


def word_occurences():
    dictionary = open('../venv/Lib/site-packages/textblob/en/en-spelling.txt', 'r')
    known_words = [word.split()[0] for word in dictionary.readlines()]

    jsonfile = open('LabeledData/LabeledTweets.json', 'r')
    values = json.load(jsonfile)
    jsonfile.close()

    unigram = {}
    tweet_number = 0
    for tweet in values['X']:
        for word in tweet.split():
            if word.isalpha() and word.lower() not in known_words:
                if word in unigram.keys():
                    unigram[word] += 15
                else:
                    unigram[word] = 10
        tweet_number += 1

    f = open("Data/crypto_unigram.txt", 'w')
    for k, v in unigram.items():
        f.write(k + " " + str(v) + "\n")
    # f.write(json.dumps(unigram, indent=0, sort_keys=True))
    f.close()


# Tweets and their respective label are stored in a json file for use by a model
def prepare_data():
    jsonfile = open('Data/Tweets.json', 'r')
    values = json.load(jsonfile)
    jsonfile.close()

    X = []
    y = []

    for tweet in values['data']:
        label = tweet['label']
        if label in ["Positive", "Neutral", "Negative"]:
            X.append(tweet['text'])
            y.append(label)

    data = {'X': X, 'y': y}
    f = open("LabeledData/LabeledTweets.json", 'w')
    f.write(json.dumps(data, indent=0, sort_keys=True))
    f.close()

    return data


# Split tweet data corresponding labels into train test and validation sets.
def train_test_validate_split(data_x, data_y):
    train_ratio = 0.70
    validation_ratio = 0.15
    test_ratio = 0.15

    # train is now 70% of the entire data set
    x_train, x_test, y_train, y_test = train_test_split(data_x, data_y,
                                                        test_size=int((len(data_x)) * test_ratio * 2), stratify=data_y)

    # test is now 15% of the initial data set
    # validation is now 15% of the initial data set
    x_val, x_test, y_val, y_test = train_test_split(x_test, y_test,
                                                    test_size=int((len(data_x)) * test_ratio), stratify=y_test)

    return x_train, x_test, x_val, y_train, y_test, y_val
