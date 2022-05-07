import spacy
import textblob
import wordsegment
import wordsegment
import re
import html.entities
from PosTagger import PosTagger
import emoji
from textblob import TextBlob

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
    rep = {" &amp; ": " & ",
           " &gt; ": " > ",
           " &lt; ": " <announcement> "}

    rep = dict((re.escape(k), v) for k, v in rep.items())
    pattern = re.compile("|".join(rep.keys()))
    translated_tweets = [pattern.sub(lambda m: rep[re.escape(m.group(0))], tweet.lower()) for tweet in tweets]
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
        if word[0] == '#':
            segments = segment_text(word)
            for x in segments:
                transformed_tweet = transformed_tweet + " " + x
        else:
            transformed_tweet = transformed_tweet + " " + word
    return transformed_tweet


def segment_text(tweet):
    return wordsegment.segment(tweet)


def remove_mentions(tweet):
    clean_tweet = ""
    for word in tweet.split():
        if word[0] != '@':
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
                        clean_tweet = clean_tweet + " " + translation[1:-1].replace("_", " ") + " "
                    else:
                        clean_tweet = clean_tweet + word[index]
            else:
                clean_tweet = clean_tweet + " " + word + " "
    return clean_tweet.replace("  ", " ")


def translate_abbreviations_slang(tweet):
    rep = {" ath ": " all time high ",
           " hodl ": " hold on for dear life ",
           " htf ": " higher time frame ",
           " ltf ": " lower time frame ",
           " btc ": " bitcoin ",
           " ada ": " cardano ",
           " eth ": " ethereum ",
           " usdt ": " tether ",
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
           " algo ": " algorithm "}

    rep = dict((re.escape(k), v) for k, v in rep.items())
    pattern = re.compile("|".join(rep.keys()))
    translated_tweet = pattern.sub(lambda m: rep[re.escape(m.group(0))], tweet.lower())
    return translated_tweet


def spelling_correction(tweet):
    return TextBlob(tweet).correct()


# set_up()
# print(segment("thisisatest"))