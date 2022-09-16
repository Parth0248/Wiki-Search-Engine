import sys
import shutil
import os
import math
import re
import xml.sax
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import FreqDist
import numpy as np
import pandas as pd
import time
from collections import defaultdict

total_docs = 470001
i = 1
div = 1
f_name = "./temp/t" + str(div) + ".txt"
sav = open(f_name,'w+')
with open("./temp/titles.txt",'r') as f:
    for line in f:
        if i > 1 and i % 10000 == 1:
            print(i)
            sav.close()
            div += 1
            f_name = "./temp/t" + str(div) + ".txt"
            sav = open(f_name,'w+')
        while (line.split(':')[0]) != str(i):
            if i > 1 and i % 10000 == 1:
                print(i)
                sav.close()
                div += 1
                f_name = "./temp/t" + str(div) + ".txt"
                sav = open(f_name,'w+')
            sav.write(str(i)+":NAN:4708\n")
            i+=1         
        sav.write(line)
        i+=1