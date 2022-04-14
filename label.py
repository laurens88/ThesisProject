import json
import pandas as pd
import random
from datetime import datetime
import os


#  Samples tweets from Tweets.json based on their rank value and converts them to a csv file for annotation in Lighttag
def split_convert():
    jsonfile = open('Data/Tweets.json', 'r')
    values = json.load(jsonfile)
    jsonfile.close()

    not_labeled = []

    tweets = len(values['data'])
    for i in range(0, tweets):
        if values['data'][i]['label'] == "?" and values['data'][i]['rank'] > 0:
            not_labeled.append(i)

    samples = random.choices(not_labeled, k=min(50, len(not_labeled)))

    data = []
    for tweet in range(0, len(samples)):
        data.append({'id': str(values['data'][samples[tweet]]['id']),
                     'text': values['data'][samples[tweet]]['text'],
                     'label': "?"})
    df = pd.DataFrame(data)
    filename = "LabeledData/"+datetime.now().strftime("%d-%m-%H-%M")+".csv"
    df.to_csv(filename)
    print(f"{filename} generated.")


# Reset all labels in Tweets.json back to '?'
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


# Print how many tweets of every label are currently in Tweets.json
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


# Extract labels from lighttag files in 'LabeledData' folder and insert them into Tweets.json
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

