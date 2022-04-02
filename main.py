#  Laurens de Bruin Radboud University s1002199
import label
import request
import json


def main():
    #request.request(100)  # Pull
    #request.merge()  # Merge json tweet files
    label.convert()  # Prepare for lighttag
    #label.insert_labels()  # Finalize data


if __name__ == '__main__':
    main()
