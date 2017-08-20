import sys
import re
import os
import collections
import csv
import math
import operator
import glob
import nltk
import itertools
from sklearn.cluster import DBSCAN
#from textblob import TextBlob as tb
from nltk.stem import WordNetLemmatizer
from nltk.stem.lancaster import LancasterStemmer
#w = sys.argv[1] 
lancaster_stemmer = LancasterStemmer()
#a = lancaster_stemmer.stem(w)
from nltk.corpus import wordnet as wn

wordnet_lemmatizer = WordNetLemmatizer()
#wordnet_lemmatizer.lemmatize("dogs")

def remove_non_ascii(text):
    text = re.sub(r'[\357\254\200]+', 'ff', text)
    text = re.sub(r'[\357\254\201]+', 'fi', text)
    text = re.sub(r'[\357\254\202]+', 'fl', text)
    text = re.sub('fffi ', 'fi', text)
    text = re.sub('fff ', 'f', text)
    text = re.sub('fff', 'f', text)
    text = re.sub('-\n','', text)
    text = re.sub('[^0-9a-zA-Z]+', ' ', text)
 #   text = re.sub(r'[^\x00-\x7F]+',' ', text) 
    return(text)


def tf(word, blob):
    return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob.words)

def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

       


import RAKE
###txt_dir = sys.argv[2]
###kw_file = sys.argv[1]
def txt2keyphrases(txt_dir, kw_file):
    ro = RAKE.Rake("./stopwords_long.txt")
    glob_keywords_file = {}
    glob_files = set()
    glob_keyword = set()
    freq =  6
    length = 4
    n_file=0
    for f in glob.glob(txt_dir + "/" + "*.txt"):
        with open(f, 'r') as content_file:
            content = content_file.read()
        n_file = n_file+1
        print(n_file)
        content = remove_non_ascii(content) 
        content = " ".join(content.split())
        mytext = " ".join(content.split())
        keywords = ro.run(mytext)
        print(f)
        short_keywords = [k for (k,v) in keywords if len(k.split()) > 0 and v > freq and len(k.split())<length]
        #import pdb; pdb.set_trace()
        paper = os.path.basename(f)
        short_kw_dict = {(paper,k):v for (k,v) in keywords if len(k.split())>0  and v > freq and len(k.split())<length}
        #short_kw_list = {k:v for (k,v) in keywords if len(k) < 30 and v > 3}
        #for (f,k),v in short_kw.iteritems():
        glob_keyword |= set(short_keywords)
        glob_files.add(os.path.basename(paper))
        glob_keywords_file.update(short_kw_dict)


    print(len(glob_keyword))
    print(len(glob_files))
    list_zeros = [["" for n in xrange(len(glob_files)+3)] for _ in xrange(len(glob_keyword)+1)]
    for (y,f) in enumerate(glob_files):
        list_zeros[0][y+2]=f
        for (x,k) in enumerate(glob_keyword):
            list_zeros[x+1][0]=k
            if (f, k) in glob_keywords_file:
                list_zeros[x+1][y+2] = glob_keywords_file[(f,k)] 
                #            print(glob_keywords_file[(f,k)])
            else:
                list_zeros[x+1][y+2] = 0
 
    final_list = []
    final_keywords = []
    print("Zosia")
    for n_row in xrange(len(list_zeros)):
        importance = sum(1 for x in list_zeros[n_row] if x > 0)
        if importance > 6: #6
            final_list.append(list_zeros[n_row])
            final_keywords.append(list_zeros[n_row][0])

    with open(kw_file, 'w') as kw_output:
        #for i in xrange(len(glob_files)):
        #    kw_output.write(list[k])
        #kw_output.write(short_kw)
        w = csv.writer(kw_output)
        w.writerows(final_list)
        
