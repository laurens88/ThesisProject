#  Laurens de Bruin Radboud University s1002199
import label
import request
import json
import time


def main():
    # while True:
    #     request.request(100)  # Pull
    #     time.sleep(600)

    request.merge()  # Merge json tweet files
    request.rank()
    #label.convert()  # Prepare for lighttag
    #label.insert_labels()  # Finalize data
    #label.reset_labels()
    #label.split_convert()


if __name__ == '__main__':
    main()
