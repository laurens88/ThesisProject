#  Laurens de Bruin Radboud University s1002199
import label
import data
import model
from Tokenizer import Tokenizer
import Preprocessor
import json
import time
import os
import datetime
import emoji


def main():
    # while datetime.datetime.now().hour != 4:
    #     data.request(100)  # Pull
    #     time.sleep(61)
    #     data.request_media(100)
    #     time.sleep(61)
    #     data.request_neg(100)
    #     time.sleep(1800)
    #
    # data.merge()  # Merge json tweet files
    # data.rank()

    # label.split_convert()
    # label.insert_labels()  # Finalize data
    # label.count_labels()
    # data.rank_distribution()
    # data.split_classes()

    model_input = data.prepare_data()
    X = model_input['X']
    y = model_input['y']
    x_train, x_test, x_val, y_train, y_test, y_val = data.train_test_validate_split(X, y)
    x_train = Preprocessor.normalize_text(x_train)
    x_test = Preprocessor.normalize_text(x_test)
    x_val = Preprocessor.normalize_text(x_val)

    # At this point the data is going to be split into two versions for the two models

    t = Tokenizer(True)

    # Preprocessor.set_up()
    # print(x_train[0])
    # Preprocessor.segment_hashtags(x_train[0])
    #Preprocessor.viterbi_pos_tagging()
    # print("Sentiment-aware tokenizer: ", Tokenizer.tokenize(t, "I like bitcoin"))
    # print("Bert tokenizer ", model.bert_tokenize("I like bitcoin"))


    print(model.classify(["I hate you", "I love you", "Bitcoin is a currency"]))



if __name__ == '__main__':
    main()
