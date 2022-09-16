from curses.ascii import isalnum, isalpha
from enum import unique
from pydoc import doc
# from numba import jit
import sys
import shutil
import os
import re
from typing import OrderedDict, final
from urllib.request import ProxyBasicAuthHandler
import xml.sax
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import FreqDist
import numpy as np
import pandas as pd
import time
from collections import defaultdict


ps = PorterStemmer()
stop_words = set(stopwords.words('english')) 


query_file = sys.argv[1]
# with open(query_file,'r') as f:
#     print(f.readlines())

sec_ind = open('./temp/sec_ind.txt','r')
ans_write = open('queries_op.txt','w')

# @jit 
def tokenize(text):
    clean_line = re.sub(r'[^A-Za-z0-9]', ' ', text)
    temp_tok = word_tokenize(clean_line)
    temp_tok = [ps.stem(word) for word in temp_tok if word not in stop_words]
    # for words in temp_tok:
        # if words != '' and words.isalnum():
        #     # indexer(words,doc_id,"t",1,file_no)
        #     print(words)
    return temp_tok

# 1.5, 0.4, 0.001, 0.001, 0.5, 5
# @jit
def normal_score(indexes,q_no,order,scores):
    
    weights = [5,1.5,0.001,0.3,0.01,0.7]
    idf = indexes.split('#')[1]
    idf = idf.split('#')[0]
    idf = idf.replace(' ','')
    idf = float(idf)
    docs = indexes.split('{')[1]
    docs = docs.replace(' ','')
    docs = docs.split('}')[0]
    docs = docs.split(']')
    
    doc_id = ""
    for part in docs:
        if len(part) > 0:
            doc_id = part.split(':')[0]
            # print(doc_id)
            if doc_id[0] == ',':
                doc_id = doc_id[1:]
            freq = part.split(':')[1]
            freq = freq.split('[')[1]
            freq = freq.split(',')
            scr = 0.0
            for i in range(len(freq)):
                scr += (weights[i] * int(freq[i]))
            # try:
            #     scores[q_no][doc_id]
            # except:
            #     scores[q_no][doc_id]=0.0
            scores[q_no][doc_id] = (float(scr) * float(idf))
    order[len(scores[q_no])] = q_no

# check if two q_no have same doc_id



# @jit
def find_ind(query_tok):
    q_no = 0
    scores = defaultdict(dict)
    order = dict()
    for query in query_tok:
        sec_ind = open('./temp/sec_ind.txt','r')
        f_ind = ""
        # print(query)
        for line in sec_ind:
            if line.split(':')[0] > query:
                f_ind = str(int(line.split(':')[1]) - 1)
                break
        indi = open('./temp/'+f_ind+'.txt','r')
        indexes = ""
        for line in indi:
            if line.split(' ')[0] == query:
                indexes = line
                break
        indi.close()
        sec_ind.close()
        q_no+=1
        if indexes == "":
            print("No results found")
            return
        else:
            normal_score(indexes,q_no,order,scores)
    
    sm = dict(sorted(order.items(), key=lambda item: item[0])) 
    final_scores = dict()

    for x in sorted(sm.values()):
        for doc_id in scores[x]:
            try:
                final_scores[doc_id] += scores[x][doc_id]
            except:
                final_scores[doc_id] = scores[x][doc_id]
    top = dict(sorted(final_scores.items(), key=lambda item: item[1], reverse=True))
    final_docs = list(top.keys())[:10]
    # print(final_docs) 
    # IMPLEMENT FASTER TITLE SEARCH USING SECONDARY INDEX
    
    for doc_id in final_docs:
        title_f = "./temp_titles/t" + str(1 + int(int(doc_id) / 10000)) + ".txt"
        title_file = open(title_f,'r')
        for line in title_file:
            if line.split(':')[0] == doc_id:
                title = line.split(':')[1:-1]
                title = ':'.join(title)
                # print(doc_id, ", ", title)
                ans_write.write(doc_id + ", " + title + '\n')
                break
        title_file.seek(0)
    title_file.close()


# @jit
def find_field_ind(line):
    tokens = dict()
    fields = ["t","b","i","c","r","l"]
    cnt = 1
    ind = ""
    l = int(len(line.split(':')))

    for part in line.split(':'):
        if cnt == 1:
            ind = part
            cnt+=1
        elif cnt == l:
            tokens[ind] = part
        else:
            tokens[ind] = part[:-2]
            ind = part[-1]
            cnt+=1
    temp_tok = dict()
    for keys in tokens.keys():
        temp_tok[keys] = tokenize(tokens[keys])

    scores = defaultdict(dict)
    for key in temp_tok.keys():
        for query in temp_tok[key]:
            sec_ind = open('./temp/sec_ind.txt','r')
            f_ind = ""
            for line in sec_ind:
                if line.split(':')[0] > query:
                    f_ind = str(int(line.split(':')[1]) - 1)
                    break
            indi = open('./temp/'+f_ind+'.txt','r')
            indexes = ""
            for line in indi:
                if line.split(' ')[0] == query:
                    indexes = line
                    break
            indi.close()
            sec_ind.close()
            if indexes == "":
                print("No results found")
                return
            else:
                weighted_score(indexes,scores,key)
    

    sm = dict(sorted(scores.items(), key=lambda item: item[0], reverse=True))


    final_scores = dict()
    for field in sm.keys():
        for doc_id in sm[field]:
            try:
                final_scores[doc_id] += sm[field][doc_id]
            except:
                final_scores[doc_id] = sm[field][doc_id]
    top = dict(sorted(final_scores.items(), key=lambda item: item[1], reverse=True))
    final_docs = list(top.keys())[:10]
    # # IMPLEMENT FASTER TITLE SEARCH USING SECONDARY INDEX

    for doc_id in final_docs:
        title_f = "./temp_titles/t" + str(1 + int(int(doc_id) / 10000)) + ".txt"
        title_file = open(title_f,'r')
        for line in title_file:
            if line.split(':')[0] == doc_id:
                title = line.split(':')[1:-1]
                title = ':'.join(title)
                # print(doc_id, ", ", title)
                ans_write.write(doc_id + ", " + title + '\n')
                break
        title_file.seek(0)
    
    title_file.close()

        
# @jit 
def weighted_score(indexes,scores,key):
    weights = [5,1.5,0.001,0.3,0.01,0.7]
    indd = 0
    if key == "t":
        indd = 0
    elif key == "i":
        indd = 1
    elif key == "b":
        indd = 2
    elif key == "l":
        indd = 3
    elif key == "r":
        indd = 4
    elif key == "c":
        indd = 5

    weights[indd]+= 150
    idf = indexes.split('#')[1]
    idf = idf.split('#')[0]
    idf = idf.replace(' ','')
    idf = float(idf)
    docs = indexes.split('{')[1]
    docs = docs.replace(' ','')
    docs = docs.split('}')[0]
    docs = docs.split(']')
    
    doc_id = ""
    for part in docs:
        if len(part) > 0:
            doc_id = part.split(':')[0]
            # print(doc_id)
            if doc_id[0] == ',':
                doc_id = doc_id[1:]
            freq = part.split(':')[1]
            freq = freq.split('[')[1]
            freq = freq.split(',')
            scr = 0.0
            for i in range(len(freq)):
                scr += (weights[i] * int(freq[i]))
            scores[key][doc_id] = (float(scr) * float(idf))
    


qer = open(query_file,'r')
for line in qer:
    check = re.split(':',line.casefold())
    t1 = time.time()
    if len(check) == 1:
        find_ind(tokenize(line))
    else:
        find_field_ind(line)
    t2 = time.time()
    ans_write.write("Time taken: " + str(t2-t1) + " seconds\n\n")
    # print("Time taken: ",t2-t1)
