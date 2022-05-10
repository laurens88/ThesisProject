import tensorflow as tf
from transformers import pipeline, BertTokenizer


def classify(tweets):
    sentiment_pipeline_base = pipeline(task="sentiment-analysis", model="finiteautomata/bertweet-base-sentiment-analysis")
    sentiment_pipeline_preprocessed = pipeline(task="sentiment-analysis", model="laurens88/finetuning-crypto-tweet-sentiment-test")
    return sentiment_pipeline_base(tweets), sentiment_pipeline_preprocessed(tweets)


def label_dist(model):
    labels = model
    pos, neg, neu = 0, 0, 0
    for l in labels:
        label = l['label']
        if label == "POS":
            pos += 1
        elif label == "NEG":
            neg += 1
        elif label == "NEU":
            neu += 1
    print("Base bert results:")
    print(f"Positive: {pos}\nNeutral: {neu} \nNegative: {neg} \n")


def bert_tokenize(data):
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    return tokenizer.tokenize(data)





