#  Laurens de Bruin Radboud University s1002199
import label
import request
import json
import time
import os
import datetime


def main():
    # while datetime.datetime.now().hour != 4:
    #     request.request(100)  # Pull
    #     time.sleep(61)
    #     request.requestMedia(100)
    #     time.sleep(61)
    #     request.requestNeg(100)
    #     time.sleep(1800)
    #
    # request.merge()  # Merge json tweet files
    #request.rank()
    #label.convert()  # Prepare for lighttag
    label.insert_labels()  # Finalize data
    #label.reset_labels()
    #label.split_convert()
    label.count_labels()


if __name__ == '__main__':
    main()
