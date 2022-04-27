import tensorflow as tf
from transformers import pipeline, AutoTokenizer


def classify():
    sentiment_pipeline = pipeline(task="sentiment-analysis", model="finiteautomata/bertweet-base-sentiment-analysis")
    data = ["I love you", "I hate you"]
    sentiment_pipeline(data)


def bert_tokenize(data):
    tokenizer = AutoTokenizer.from_pretrained("distilbert-base-cased")
    tokenizer(data)





