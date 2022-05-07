import tensorflow as tf
from transformers import pipeline, BertTokenizer


def classify(tweets):
    sentiment_pipeline = pipeline(task="sentiment-analysis", model="finiteautomata/bertweet-base-sentiment-analysis")
    return sentiment_pipeline(tweets)


def bert_tokenize(data):
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    return tokenizer.tokenize(data)





