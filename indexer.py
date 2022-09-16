import sys
import shutil
import os
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
# infobox splitting done
# category splitting done
# title splitting donetostring
# reference links left

total_tokens = 0
saved_tokens = 0

stop_words = set(stopwords.words('english'))
ps = PorterStemmer()
inverse_index = dict()
inv_ind = defaultdict(dict)
titles = defaultdict(dict)

# kinda finished splitting data to category wise lists of lines
def split(title,text,doc_id,file_no):
    
    infobox = []
    category = []
    link = []
    reference = []
    body = []
        
    flags = [0,0,0,0]
    sep = text.split('\n')
    lines = [sentence.casefold() for sentence in sep]

    for line in lines:
        if re.match(r'\{\{infobox',line) != None:
            # reset(flags)
            flags[0] = 1
        elif re.match(r'\[\[category:(.*)\]\]',line) != None:
            # reset(flags)
            flags[1] = 1
        elif re.match(r'\=\=external links\=\=',line) != None:
            # reset(flags)
            flags[2] = 1
            continue;
        elif re.match(r'\=\=references\=\=',line) != None:
            # reset(flags)
            flags[3] = 1
            continue; 

        if flags[0] :
            if line == "}}":
                flags[0] = 0
                continue;
            # infobox.append(re.split('\=',line)[1])
            if re.search(r'^\|',line) != None:
                clean_line = re.sub(r'\=','',line)
                infobox.append(clean_line[1:])
            # info_split = re.split('\=',line)
            # if len(info_split) >= 2 and info_split[1] != '':
            #     clean_line = re.sub(r'[^A-Za-z0-9]+', ' ', info_split[1])
            #     infobox.append(clean_line)
                        
        elif flags[1] == 1:
            cat_split = re.split('\:',line)
            if len(cat_split) == 2 and cat_split[1] != '':
                clean_line = re.sub(r'[^A-Za-z0-9]+', ' ', cat_split[1])
                category.append(clean_line)
            flags[1] = 0

        elif flags[2] == 1:
            if line and line[0] == '*':
                clean_line = re.sub(r'[^A-Za-z0-9]+', ' ', line)
                link.append(clean_line)
            else:
                flags[2] = 0
        
        elif flags[3] == 1:
            if line and line[0] == '*':
                clean_line = re.sub(r'[^A-Za-z0-9]+', ' ', line)
                reference.append(clean_line)
            else:
                flags[3] = 0
        
        else:
            clean_line = re.sub(r'[^A-Za-z0-9]+', ' ', line)
            body.append(clean_line)
            
    process(title,'title',doc_id,file_no)
    process(infobox,'infobox',doc_id,file_no)
    process(category,'category',doc_id,file_no)
    process(body,'body',doc_id,file_no)
    process(reference,'ref',doc_id,file_no)
    process(link,'link',doc_id,file_no)

# 895t6i4b7r2l2 ===> Sample Index


def indexer(word,doc_id,category,freq,file_no):
    global total_tokens
    word = word.casefold()
    total_tokens+=1
    # print(word,category,doc_id)
    if category == "t":
        try:
            inv_ind[word][doc_id]
        except:
            inv_ind[word][doc_id]=[0,0,0,0,0,0]
        
        inv_ind[word][doc_id][0]+=1

    elif category == "i":
        try:
            inv_ind[word][doc_id]
        except:
            inv_ind[word][doc_id]=[0,0,0,0,0,0]
        
        inv_ind[word][doc_id][1]+=1

    elif category == "b":
        try:
            inv_ind[word][doc_id]
        except:
            inv_ind[word][doc_id]=[0,0,0,0,0,0]
        
        inv_ind[word][doc_id][2]+=1
    
    elif category == "l":
        try:
            inv_ind[word][doc_id]
        except:
            inv_ind[word][doc_id]=[0,0,0,0,0,0]
        
        inv_ind[word][doc_id][3]+=1

    elif category == "r":
        try:
            inv_ind[word][doc_id]
        except:
            inv_ind[word][doc_id]=[0,0,0,0,0,0]
        
        inv_ind[word][doc_id][4]+=1

    elif category == "c":
        try:
            inv_ind[word][doc_id]
        except:
            inv_ind[word][doc_id]=[0,0,0,0,0,0]
        
        inv_ind[word][doc_id][5]+=1

def indexer1(word,doc_id,category,freq):
    if word in inverse_index:
        temp_value = inverse_index[word].split(';')[-1]
        last_doc_id = re.match(r'^[0-9]*',temp_value).group()
        if last_doc_id != doc_id:
            temp_entry = ";" + doc_id + category + str(freq)
            inverse_index[word] = inverse_index[word] + temp_entry
        else:
            temp_entry = category + str(freq)
            inverse_index[word] = inverse_index[word] + temp_entry
    else:
        inverse_index[word] = doc_id + category + str(freq)

# tokenize list of clean strings for each category and call function that writes to file
def process(item,category,doc_id,file_no):
        
    if category == 'title':
        clean_line = re.sub(r'[^A-Za-z0-9]', ' ', item)
        temp_tok = word_tokenize(clean_line)
        temp_tok = [ps.stem(word) for word in temp_tok if word not in stop_words]
        for words in temp_tok:
            if words != '' and words.isalnum():
                indexer(words,doc_id,"t",1,file_no)

    elif category == 'category':
        temp_tok = [word_tokenize(x) for x in item]
        temp_tok1 = [] # list of words of category field
        for lines in temp_tok:
            temp_tok1 = [ps.stem(word) for word in lines if word not in stop_words]
        for words in temp_tok1:
            if words != '' and words.isalnum():
                indexer(words,doc_id,"c",1,file_no)

    elif category == 'link':
        temp_tok = [word_tokenize(x) for x in item]
        temp_tok1 = [] # list of words of links field
        for lines in temp_tok:
            temp_tok1 = [ps.stem(word) for word in lines if word not in stop_words]
        for words in temp_tok1:
            if words != '' and words.isalnum():
                indexer(words,doc_id,"l",1,file_no)

    elif category == 'infobox':
        temp_tok = [word_tokenize(x) for x in item]
        temp_tok1 = [] # list of words of infobox field
        for lines in temp_tok:
            temp_tok1 = [ps.stem(word) for word in lines if word not in stop_words]
        for words in temp_tok1:
            if words != '' and words.isalnum():
                indexer(words,doc_id,"i",1,file_no)

    elif category == 'ref':
        temp_tok = [word_tokenize(x) for x in item]
        temp_tok1 = []
        for lines in temp_tok:
            temp_tok1 = [ps.stem(word) for word in lines if word not in stop_words]
        for words in temp_tok1:
            if words != '' and words.isalnum():
                indexer(words,doc_id,"r",1,file_no)

    elif category == 'body':
        temp_tok = [word_tokenize(x) for x in item]
        temp_tok1 = []
        for lines in temp_tok:
            temp_tok1 = [ps.stem(word) for word in lines if word not in stop_words]
        for words in temp_tok1:
            if words != '' and words.isalnum():
                indexer(words,doc_id,"b",1,file_no)


def seg(name):
    f_name = './temp1/' + str(name) + ".txt"
    f = open(f_name,'w+')
    
    for key in sorted(inv_ind.keys()):
        f.write('%s:%s\n' % (key, inv_ind[key]))
    
    ti_name = './temp1/' + "titles" + ".txt"
    if os.path.exists(ti_name) == 0:
         ti = open(ti_name,'w+')       
    else:
        ti = open(ti_name,'a')

    for keys in titles.keys():
        ti.write('%s:%s\n' % (keys, titles[keys]))
    
    ti.close()
    f.close()
    inv_ind.clear()
    titles.clear()

class WikiHandler(xml.sax.ContentHandler):
    global PageCnt
    def __init__(self):
        self.current = ''
        self.title = ''
        self.text = ''
        self.doc_count = 1
        self.file_count = 1

    def startElement(self,name,attrs):
        self.current = name

    def characters(self, content):
        if self.current == 'title':
            self.title += content
        elif self.current == 'text':
            self.text += content
            

    def endElement(self,name):
        if name == 'title':
            titles[self.doc_count] = str(self.title)
        if name == 'text':
            split(self.title,self.text,self.doc_count,self.file_count)
            if self.doc_count > 1 and self.doc_count % 10000 == 1:
                seg(self.file_count)
                print(self.file_count)
                self.file_count+=1

            self.doc_count += 1
            self.text = ''
            self.title = ''
        
# contenthandler to read wiki xml file

t1 = time.time()

# if os.path.exists("./temp") == 0:
#     os.mkdir("./temp")

parser = xml.sax.make_parser()
parser.setFeature(xml.sax.handler.feature_namespaces,0)
handler = WikiHandler()
parser.setContentHandler(handler)
parser.parse(sys.argv[1])

        
# keep a record to maintiain invertedindex_stat.txt
try:
    shutil.rmtree(sys.argv[2])
    os.mkdir(sys.argv[2])
except:
    os.mkdir(sys.argv[2])
    
# dump = open(sys.argv[1],'r')
ind = open(sys.argv[3],'w')
saved_tokens = len(inv_ind)
ind.write(str(total_tokens) + '\n' + str(saved_tokens))

# with open(file_path, 'w') as f: 
# cur = 'a'
# mid = 'm'
# flag = True
# file_path = os.path.join(sys.argv[2],"num.txt")
# f = open(file_path,'w')
# for key in sorted(inv_ind.keys()): 
#     if key[0] == cur:
#         flag = True
#         f_name = str(key[0]) + "1.txt" 
#         file_path = file_path = os.path.join(sys.argv[2],f_name)
#         f.close()
#         f = open(file_path,'w')
#         cur = chr(ord(cur) + 1)
#     if(ord(key[0]) == ord(cur)-1 and flag and len(key)>1 and ord(key[1]) >= ord(mid)):
#             flag = False
#             f_name = str(key[0]) + "2.txt"
#             file_path = file_path = os.path.join(sys.argv[2],f_name)
#             f.close()
#             f = open(file_path,'w')
#     f.write('%s:%s\n' % (key, inv_ind[key]))

t2 = time.time()
print(t2-t1)
print("index_made")