import json
import pandas as pd
from pathlib import Path
import numpy as np
import random
from datetime import datetime
import os

#  Convert output json file from pull request to csv file. Csv file uploaded to lighttag
#  Also returns the pandas dataframe and the number of tweets


def convert():
    jsonfile = open('Data/05-04-09-09.json', 'r')
    values = json.load(jsonfile)
    jsonfile.close()
    tweets = len(values['data'])

    input_tweets = []
    labels = []
    ids = []

    for tweet in range(0, tweets):
        tweet_id = str(values['data'][tweet]['id'])
        ids.append(tweet_id)
        text = values['data'][tweet]['text']
        input_tweets.append(text)
        labels.append("")
    data = {'id': ids, 'tweet': input_tweets, 'label': labels}
    df = pd.DataFrame(data)  # Use this for the model (Labels missing here)

    filename = "LabeledData/Test.csv"
    filepath = Path(filename)
    df.to_csv(filepath)

    return data, tweets


def split_convert():
    jsonfile = open('Data/Tweets.json', 'r')
    values = json.load(jsonfile)
    jsonfile.close()

    not_labeled = []

    tweets = len(values['data'])
    for i in range(0, tweets):
        if values['data'][i]['label'] == "?":
            not_labeled.append(i)

    samples = random.choices(not_labeled, k=min(50, len(not_labeled)))

    data = []
    for tweet in range(0, len(samples)):
        data.append({'id': str(values['data'][samples[tweet]]['id']), 'text': values['data'][samples[tweet]]['text'], 'label': "?"})
    df = pd.DataFrame(data)
    filename = "LabeledData/"+datetime.now().strftime("%d-%m-%H-%M")+".csv"
    df.to_csv(filename)
    print(f"{filename} generated.")


def reset_labels():
    jsonfile = open('Data/Tweets.json', 'r')
    values = json.load(jsonfile)
    jsonfile.close()

    tweets = len(values['data'])
    for i in range(0, tweets):
        values['data'][i]['label'] = "?"

    f = open("Data/Tweets.json", 'w')
    f.write(json.dumps(values, indent=0, sort_keys=True))
    f.close()


def count_labels():
    jsonfile = open('Data/Tweets.json', 'r')
    values = json.load(jsonfile)
    jsonfile.close()

    tweets = len(values['data'])
    pos, neg, neu = 0, 0, 0
    for i in range(tweets):
        label = values['data'][i]['label']
        if label == "Positive":
            pos += 1
        elif label == "Negative":
            neg += 1
        elif label == "Neutral":
            neu += 1
    print(f"Positive: {pos}\nNeutral: {neu} \nNegative: {neg} \n")


#  Test function to display the content of pulled Tweets
def display(filename, limit):
    jsonfile = open(filename, 'r')
    values = json.load(jsonfile)
    jsonfile.close()
    tweets = len(values['data'])

    for tweet in range(0, min(tweets, limit)):
        print(values['data'][tweet]['text'])
        print("----------------")


# Insert labels from lighttag into Tweets.json
def insert_labels():
    jsonfile = open('Data/Tweets.json', 'r')
    tweets = json.load(jsonfile)
    jsonfile.close()
    n_tweets = len(tweets['data'])

    directory = "LabeledData"

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f) and filename.endswith('.json'):
            jsonfile = open(f, 'r', encoding="utf8")
            annotations = json.load(jsonfile)
            jsonfile.close()

            n_labels = len(annotations['examples'])

            # Match tweets by tweet id and set label
            for annotation in range(n_labels):
                tweet_id = annotations['examples'][annotation]['metadata']['id']
                label = annotations['examples'][annotation]['classifications'][0]['classname']
                for tweet in range(n_tweets):
                    if tweets['data'][tweet]['id'] == tweet_id:
                        tweets['data'][tweet]['label'] = label

    f = open("Data/Tweets.json", 'w')
    f.write(json.dumps(tweets, indent=0, sort_keys=True))
    f.close()

    print("Labels inserted into Tweets.json")


def main():
    convert()
    #insert_labels()


if __name__ == '__main__':
    main()
