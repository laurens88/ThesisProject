#  Laurens de Bruin Radboud University s1002199
import label
import request
import json
import time


def main():
    # i = 0
    # while i < 10:
    #     request.request(100)  # Pull
    #     request.merge()  # Merge json tweet files
    #     i = i+1
    #     time.sleep(600)
    label.convert()  # Prepare for lighttag
    #label.insert_labels()  # Finalize data


if __name__ == '__main__':
    main()
