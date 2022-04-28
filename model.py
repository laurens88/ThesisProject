import tensorflow as tf
from transformers import pipeline, AutoTokenizer


def classify(tweets):
    sentiment_pipeline = pipeline(model="finiteautomata/bertweet-base-sentiment-analysis")
    return sentiment_pipeline(tweets)

def bert_tokenize(data):
    tokenizer = AutoTokenizer.from_pretrained("distilbert-base-cased")
    tokenizer(data)





