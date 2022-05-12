import tensorflow as tf
from transformers import pipeline, BertTokenizer
from sklearn.metrics import f1_score


def base_classify(tweets):
    sentiment_pipeline_base = pipeline(task="sentiment-analysis",
                                       model="finiteautomata/bertweet-base-sentiment-analysis")
    return sentiment_pipeline_base(tweets)


def proposed_classify(tweets):
    sentiment_pipeline_preprocessed = pipeline(task="sentiment-analysis",
                                               model="laurens88/finetuning-crypto-tweet-sentiment-test")
    return sentiment_pipeline_preprocessed(tweets)

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


def compute_f1(y_pred, y_true):
    print(f1_score(y_true, y_pred, average="macro"))


def bert_tokenize(data):
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    return tokenizer.tokenize(data)





