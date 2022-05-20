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


    jsonfile = open('LabeledData/labels.json', 'r')
    values = json.load(jsonfile)
    jsonfile.close()

    fold_labels = [data.transform_short_label_num(y['label']) for y in values]
    true_labels = [data.transform_label_num(y) for y in clean_y]

    # _, test_y = data.read_set("LabeledData/complete_set.json")
    # raw_x, _ = data.read_set("LabeledData/complete_set_raw.json")
    #
    base = model.base_classify(clean_X)
    # proposed = model.proposed_classify(test_x)
    labels1 = [data.transform_short_label_num(samples['label']) for samples in base]
    # labels2 = [data.transform_short_label_num(samples['label']) for samples in proposed]
    #
    # # true_labels = [data.transform_label_num(text_label) for text_label in clean_y]
    # true_labels = test_y
    #
    c1 = 0
    c2 = 0
    for i in range(len(labels1)):
        if labels1[i] == true_labels[i]:
            c1 += 1
        if fold_labels[i] == true_labels[i]:
            c2 += 1
    print(f"Base model accuracy: {c1 / len(labels1)}")
    print(f"Proposed model accuracy: {c2 / len(fold_labels)}" + "\n")
    # model.compute_f1(labels1, true_labels)
    # model.compute_f1(labels2, true_labels)
    print(f"f1 score base: {model.compute_f1(labels1, true_labels)}")
    print(f"f1 score proposed: {model.compute_f1(fold_labels, true_labels)}")


if __name__ == '__main__':
    main()
