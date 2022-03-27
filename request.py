import sys
import requests
import json

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
    query_params = {'query': '-has:links -@LinkSync_tech (#crypto OR #cryptocurrency OR #BTC OR XRP OR #XRP OR #ETH OR dogecoin OR cardano OR polkadot OR dogecoin OR paycoin OR altcoin) ((is down) OR (is up) OR (last hour) OR 📈 OR 📉 OR 🚀 OR (current price) OR opinion OR changes OR today OR summary) -NFT lang:en -is:retweet', 'max_results': limit}
    json_response = connect_to_endpoint(search_url, query_params)
    f = open("neu1.json", 'w')
    f.write(json.dumps(json_response, indent=0, sort_keys=True))
    f.close()
    print(f"{query_params['max_results']} tweets pulled.")


def main():
    request(10)


if __name__ == '__main__':
    main()
