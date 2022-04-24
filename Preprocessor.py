import spacy

sp = spacy.load('en_core_web_sm')


def pos_tagging(sentence):
    for token in sentence:
        sen = sp(token)
        for w in sen:
            print(sen, w, spacy.explain(w.tag_))
