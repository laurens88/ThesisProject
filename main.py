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
    model_input = data.prepare_data()  # Data without preprocessing
    X = model_input['X']
    y = model_input['y']
    x_train, x_test, x_val, y_train, y_test, y_val = data.train_test_validate_split(X, y)

    # At this point the data is going to be split into two versions for the two models

    t = Tokenizer(True)

    Preprocessor.set_up()
    Preprocessor.process_data()  # Data with preprocessing


if __name__ == '__main__':
    main()
