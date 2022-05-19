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
    raw_x = data.read_labeled()

    for i in range(1, 11):
        data.data_to_k_fold_model_format(clean_X, clean_y, i)

    # x_train, x_test, x_val, y_train, y_test, y_val = data.train_test_validate_split(clean_X, clean_y)
    #
    # data.data_to_model_format(clean_X, clean_y, "complete_set.json")
    # data.data_to_model_format(x_train, y_train, "train.json")
    # data.data_to_model_format(x_test, y_test, "test.json")
    # data.data_to_model_format(x_val, y_val, "val.json")
    # data.data_to_model_format(raw_x, clean_y, "complete_set_raw.json")

    # test_x, test_y = data.read_set("LabeledData/complete_set.json")
    # raw_x, _ = data.read_set("LabeledData/complete_set_raw.json")
    #
    # base = model.base_classify(raw_x)
    # proposed = model.proposed_classify(test_x)
    # labels1 = [data.transform_short_label_num(samples['label']) for samples in base]
    # labels2 = [data.transform_short_label_num(samples['label']) for samples in proposed]
    #
    # # true_labels = [data.transform_label_num(text_label) for text_label in clean_y]
    # true_labels = test_y
    #
    # c1 = 0
    # c2 = 0
    # for i in range(len(labels1)):
    #     if labels1[i] == true_labels[i]:
    #         c1 += 1
    #     if labels2[i] == true_labels[i]:
    #         c2 += 1
    # print(f"Base model accuracy: {c1 / len(labels1)}")
    # print(f"Proposed model accuracy: {c2 / len(labels2)}")
    # model.compute_f1(labels1, true_labels)
    # model.compute_f1(labels2, true_labels)
    # print(f"f1 score base: {model.compute_f1(labels1, clean_y)}")
    # print(f"f1 score proposed: {model.compute_f1(labels2, clean_y)}")


if __name__ == '__main__':
    main()
