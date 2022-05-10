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
    base_data = data.prepare_data()  # Data without preprocessing
    base_X = base_data['X']
    base_y = base_data['y']


    # At this point the data is going to be split into two versions for the two models

    Preprocessor.set_up()
    clean_data = Preprocessor.process_data()  # Data with preprocessing
    clean_X = clean_data['X']
    clean_y = clean_data['y']
    # x_train, x_test, x_val, y_train, y_test, y_val = data.train_test_validate_split(clean_X, clean_y)
    #
    # data.data_to_model_format(clean_X, clean_y, "complete_set.json")
    # data.data_to_model_format(x_train, y_train, "train.json")
    # data.data_to_model_format(x_test, y_test, "test.json")
    # data.data_to_model_format(x_val, y_val, "val.json")

    model1, model2 = model.classify(clean_X)
    model.label_dist(model1)
    model.label_dist(model2)


if __name__ == '__main__':
    main()
