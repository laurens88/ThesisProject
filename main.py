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

    Preprocessor.set_up()
    raw_tweet = x_train[0]
    print("Raw: ", raw_tweet)
    clean_tweet = Preprocessor.correct_spacing(
        str(Preprocessor.spelling_correction(
            Preprocessor.translate_abbreviations_slang(
                Preprocessor.segment_hashtags(
                    Preprocessor.translate_emojis(
                        Preprocessor.remove_mentions(raw_tweet)))))))
    print("|||||||||||||||||||||||||||||||||||||||||||")
    print("Processed :", clean_tweet)
    print(model.classify([raw_tweet, clean_tweet]))


if __name__ == '__main__':
    main()
