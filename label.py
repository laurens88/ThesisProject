import json
import pandas as pd
from pathlib import Path
import numpy as np
import random

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

    samples = random.choices(not_labeled, k=50)

    data = []
    for tweet in range(0, 50):
        data.append({'id': values['data'][samples[tweet]]['id'], 'text': values['data'][samples[tweet]]['text'], 'label': "?"})
    df = pd.DataFrame(data)
    df.to_csv('LabeledData/Tweets50.csv')


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


#  Test function to display the content of pulled Tweets
def display(filename, limit):
    jsonfile = open(filename, 'r')
    values = json.load(jsonfile)
    jsonfile.close()
    tweets = len(values['data'])

    for tweet in range(0, min(tweets, limit)):
        print(values['data'][tweet]['text'])
        print("----------------")


# Insert labels into csv after annotation is done in lighttag
def insert_labels():
    data, tweets = convert()
    jsonfile = open('positive/pos1_annotations.json', 'r', encoding="utf8")
    values = json.load(jsonfile)
    jsonfile.close()

    jsonfile = open('positive/pos1_use100.json', 'r')
    tweet_values = json.load(jsonfile)
    jsonfile.close()

    classnames = []
    for n in range(0, tweets):
        classnames.append("")
    for label in range(0, tweets):
        for tweet in range(0, tweets):
            if tweet_values['data'][tweet]['text'] == values['examples'][label]['content']:
                classnames[tweet] = values['examples'][label]['classifications'][0]['classname']
    data['label'] = list(classnames)
    df = pd.DataFrame(data)  # This is probably used for the model, csv is just for visual representation

    filename = "positive/pos1_annotated.csv"
    filepath = Path(filename)
    df.to_csv(filepath)

    df.to_json("positive/pos1_annotated.json")

    print(f"Annotations stored in {filename}")


def main():
    convert()
    #insert_labels()


if __name__ == '__main__':
    main()
