import spacy
import wordsegment
import wordsegment

global sp


def set_up():
    sp = spacy.load('en_core_web_sm')
    wordsegment.load()
    wordsegment.UNIGRAMS['bitcoin'] = 9e10
    wordsegment.UNIGRAMS['ath'] = 1.3e7
    wordsegment.UNIGRAMS['ethereum'] = 2e8
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


def pos_tagging(sentence):
    for token in sentence:
        sen = sp(token)
        for w in sen:
            print(sen, w, spacy.explain(w.tag_))


def segment_text(tweet):
    print(wordsegment.segment(tweet))

# set_up()
# print(segment("thisisatest"))