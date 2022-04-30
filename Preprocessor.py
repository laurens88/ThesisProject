import spacy
import wordsegment
import wordsegment
import re
import html.entities
from PosTagger import PosTagger

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
    wordsegment.UNIGRAMS['htf'] = 1e6


def normalize_text(X):
    html_entity_digit_re = re.compile(r"&#\d+;")
    html_entity_alpha_re = re.compile(r"&\w+;")
    amp = "&amp;"

    for i in range(len(X)):
        # First the digits:
        ents = set(html_entity_digit_re.findall(X[i]))
        if len(ents) > 0:
            for ent in ents:
                entnum = ent[2:-1]
                try:
                    entnum = int(entnum)
                    X[i] = X[i].replace(ent, chr(entnum))
                except:
                    pass
        # Now the alpha versions:
        ents = set(html_entity_alpha_re.findall(X[i]))
        ents = filter((lambda x: x != amp), ents)
        for ent in ents:
            entname = ent[1:-1]
            try:
                X[i] = X[i].replace(ent, chr(html.entities.name2codepoint[entname]))
            except:
                pass
            X[i] = X[i].replace(amp, " and ")
    return X


def pos_tagging(sentence):
    for token in sentence:
        sen = sp(token)
        for w in sen:
            print(sen, w, spacy.explain(w.tag_))


def viterbi_pos_tagging():
    pt = PosTagger()
    PosTagger.tag(pt)


def segment_text(tweet):
    print(wordsegment.segment(tweet))

# set_up()
# print(segment("thisisatest"))