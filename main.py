#  Laurens de Bruin Radboud University s1002199
import label
import request
import json
import time


def main():
    while True:
        time.sleep(90)
        request.request(100)  # Pull
        request.merge()  # Merge json tweet files
    #label.convert()  # Prepare for lighttag
    #label.insert_labels()  # Finalize data


if __name__ == '__main__':
    main()
