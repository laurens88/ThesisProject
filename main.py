#  Laurens de Bruin Radboud University s1002199
import label
import request
import json
import time
import os

def main():
    #request.request(100)  # Pull
    # request.merge()  # Merge json tweet files
    # request.rank()
    #label.convert()  # Prepare for lighttag
    #label.insert_labels()  # Finalize data
    #label.reset_labels()
    label.split_convert()
    #label.count_labels()


if __name__ == '__main__':
    main()
