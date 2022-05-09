import spacy
import textblob
import wordsegment
import wordsegment
import re
import html.entities
from PosTagger import PosTagger
import emoji
from textblob import TextBlob
import json

global sp


def set_up():
    sp = spacy.load('en_core_web_sm')
    wordsegment.load()
    wordsegment.UNIGRAMS['bitcoin'] = 9e10
    wordsegment.UNIGRAMS['btc'] = 9e10
    wordsegment.UNIGRAMS['ath'] = 1.3e7
    wordsegment.UNIGRAMS['ethereum'] = 2e8
    wordsegment.UNIGRAMS['eth'] = 2e8
    wordsegment.UNIGRAMS['cryptocurrency'] = 3e8
    wordsegment.UNIGRAMS['blockchain'] = 3.2e8
    wordsegment.UNIGRAMS['altcoin'] = 5e6
    wordsegment.UNIGRAMS['binance'] = 1.9e8
    wordsegment.UNIGRAMS['cryptocurrencies'] = 3e8
    wordsegment.UNIGRAMS['usdt'] = 1e7
    wordsegment.UNIGRAMS['dogecoin'] = 1e8
    wordsegment.UNIGRAMS['hodl'] = 9e5
    wordsegment.UNIGRAMS['usdt'] = 1.9e8
    wordsegment.UNIGRAMS['altcoins'] = 5e6
    wordsegment.UNIGRAMS['memecoin'] = 2e5
    wordsegment.UNIGRAMS['ai'] = 5e8
    wordsegment.UNIGRAMS['nft'] = 2.8e8
    wordsegment.UNIGRAMS['inu'] = 1e8
    wordsegment.UNIGRAMS['htf'] = 1e6
    wordsegment.UNIGRAMS['ltf'] = 1e6
    wordsegment.UNIGRAMS['bnb'] = 1e6
    wordsegment.UNIGRAMS['ta'] = 2e5
    wordsegment.UNIGRAMS['defi'] = 2e8


def normalize_text(tweets):
    rep = {"&amp;": "&",
           "&gt;": ">",
           "&lt;": "<",
           "\u2026": "...",
           "\u00a3": "£",
           "\ufe0f": " ",
           "\u2013": "-",
           "\u201c": "“",
           "\u201d": "”",
           "\u2019": "'",
           "\u20bf": "₿"}

    rep = dict((re.escape(k), v) for k, v in rep.items())
    pattern = re.compile("|".join(rep.keys()))
    translated_tweets = [pattern.sub(lambda m: rep[re.escape(m.group(0))], tweet) for tweet in tweets]
    return translated_tweets


def pos_tagging(sentence):
    for token in sentence:
        sen = sp(token)
        for w in sen:
            print(sen, w, spacy.explain(w.tag_))


def viterbi_pos_tagging():
    pt = PosTagger()
    PosTagger.tag(pt)


def segment_hashtags(tweet):
    transformed_tweet = ""
    for word in tweet.split():
        if word[0] == '#' or (word[0] == '$' and not has_numbers(word)):
            segments = segment_text(word)
            for x in segments:
                transformed_tweet = transformed_tweet + " " + x
        else:
            transformed_tweet = transformed_tweet + " " + word
    return transformed_tweet


def has_numbers(text):
    return any(char.isdigit() for char in text)


def segment_text(tweet):
    return wordsegment.segment(tweet)


def clean_mentions_urls(tweet):
    clean_tweet = ""
    for word in tweet.split():
        if word[0] == '@':
            clean_tweet = clean_tweet + " " + "@USER"
        elif word[0:4] == 'http':
            clean_tweet = clean_tweet + " " + "HTTPURL"
        else:
            clean_tweet = clean_tweet + " " + word
    return clean_tweet


def translate_emojis(tweet):
    if not emoji.emoji_lis(tweet):
        return tweet
    else:
        clean_tweet = ""
        for word in tweet.split():
            emoji_locations = [e['location'] for e in emoji.emoji_lis(word)]
            if emoji_locations:
                for index in range(len(word)):
                    if index in emoji_locations:
                        translation = emoji.demojize(word[index])
                        clean_tweet = clean_tweet + " " + translation + " "
                    else:
                        clean_tweet = clean_tweet + word[index]
            else:
                clean_tweet = clean_tweet + " " + word + " "
    return clean_tweet


def translate_abbreviations_slang(tweet):
    rep = {" ath ": " all time high ",
           " hodl ": " hold on for dear life ",
           " htf ": " higher time frame ",
           " ltf ": " lower time frame ",
           "btc": " bitcoin ",
           "BTC": " Bitcoin ",
           " ada ": " cardano ",
           " ADA ": " Cardano",
           " eth ": " ethereum ",
           " ETH ": " Ethereum ",
           " usdt ": " tether ",
           " USDT ": " Tether",
           "xrp": " ripple ",
           "XRP": " Ripple ",
           " doge ": " dogecoin ",
           " DOGE ": " Dogecoin",
           "bnb": " binance ",
           "BNB": " Binance",
           " sol ": " solana ",
           " SOL ": " Solana ",
           " ta ": " technical analysis ",
           " ann ": " announcement ",
           " avg ": " average ",
           " apr ": " april ",
           " bpi ": " bitcoin price index ",
           " bro ": " brother ",
           " cmon ": " come on ",
           " Im ": " I'm ",
           " macd ": " moving average convergence divergence indicator",
           " stfu ": " shut the fuck up",
           " wtf ": " what the fuck ",
           " mfs ": " motherfuckers ",
           " ur ": " your ",
           " af ": " as fuck ",
           " algo ": " algorithm ",
           " uber ": " very ",
           " mkt ": " market ",
           " chg ": " change "}

    rep = dict((re.escape(k), v) for k, v in rep.items())
    pattern = re.compile("|".join(rep.keys()))
    translated_tweet = pattern.sub(lambda m: rep[re.escape(m.group(0))], tweet)
    prices = [m.span() for m in re.finditer(' \d+k', translated_tweet)]
    offset = 0
    for i in prices:

        pos = i[-1]-1 + offset
        new_char = '.000 '

        temp = list(translated_tweet)
        temp[pos] = new_char
        translated_tweet = "".join(temp)
        offset += 4

    prices2 = [m.span() for m in re.finditer('\d+[,|.]?\d*k', translated_tweet)]
    offset = 0
    for i in prices2:
        pos = i[-1] - 1 + offset
        new_char = '00 '

        temp = list(translated_tweet)
        temp[pos] = new_char
        translated_tweet = "".join(temp)
        offset += 3

    return translated_tweet


def spelling_correction(tweet):
    return TextBlob(tweet).correct()


def correct_spacing(tweet):
    return tweet.replace("  ", " ")


def process_data():
    jsonfile = open('LabeledData/LabeledTweets.json', 'r')
    values = json.load(jsonfile)
    jsonfile.close()

    X = values['X']
    y = values['y']

    # x_clean = normalize_text([correct_spacing(
    #             translate_abbreviations_slang(
    #                 segment_hashtags(
    #                     translate_emojis(
    #                         clean_mentions_urls(tweet))))) for tweet in X])
    x_clean = normalize_text([correct_spacing(translate_abbreviations_slang(segment_hashtags(translate_emojis(clean_mentions_urls(tweet))))) for tweet in X])

    data = {'X': x_clean, 'y': y}

    f = open("LabeledData/LabeledProcessedTweets.json", 'w')
    f.write(json.dumps(data, indent=0, sort_keys=True))
    f.close()


