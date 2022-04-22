#  Laurens de Bruin Radboud University s1002199
import label
import data
import model
from Tokenizer import Tokenizer
import json
import time
import os
import datetime


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
    x_train, x_test, x_val, y_train, y_test, y_val = model.train_test_validate_split(X, y)
    t = Tokenizer(True)
    print(list(Tokenizer.tokenize(t, x_train[0])))


if __name__ == '__main__':
    main()
