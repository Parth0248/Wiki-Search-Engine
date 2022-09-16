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

total_docs = 22280001
i = 1
div = 1
f_name = "./temp/" + str(div) + ".txt"
sav = open(f_name,'w+')
sec_ind = open('./temp/sec_ind.txt','w+')
with open("./merge/temp_final.txt",'r') as f:
    for line in f:
        if i > 1 and i % 15000 == 1:
            sav.close()
            div += 1
            f_name = "./temp/" + str(div) + ".txt"
            sav = open(f_name,'w+')
              
        idf = math.log(total_docs / (len(line.split(','))/6))
        line = line.split(':')
        if i % 15000 == 1:
            sec_ind.write(line[0]+':'+ str(div)+'\n')    
        line[0] += ' # ' + str(idf) + ' # '
        sav.write(':'.join(line))
        i+=1

        