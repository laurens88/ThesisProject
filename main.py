#  Laurens de Bruin Radboud University s1002199
import label
import request
import json
import time


def main():
    #request.request(100)  # Pull
    #request.merge()  # Merge json tweet files
    #label.convert()  # Prepare for lighttag
    #label.insert_labels()  # Finalize data
    #label.reset_labels()
    label.split_convert()


if __name__ == '__main__':
    main()
