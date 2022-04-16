#  Laurens de Bruin Radboud University s1002199
import label
import data
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
    label.insert_labels()  # Finalize data
    label.count_labels()
    #data.rank_distribution()


if __name__ == '__main__':
    main()
