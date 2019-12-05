
import math
import csv
import re
import os
import pandas as pd

def main(name):
    urls = pd.read_csv("./hotel_links/" + name)

    df = urls.drop_duplicates('Link')

    df.to_csv('./new/' + name,index=False)


if __name__ == '__main__':
    path = "./hotel_links"
    file_list = os.listdir(path)

    for file in file_list:
        main(file)