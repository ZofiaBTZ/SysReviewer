"""Script to run through new cleanse and RAKE logic"""
import os
import time
import requests
from bs4 import BeautifulSoup
import RAKE
import re
import glob
import tfidf
import sys
import csv
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import brown
import math

#RAKE_STOPLIST = './Malawi_search_words/stopwords_long_tfidf.txt'
CACHE_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'cache')

#Removes non ASCII characters
def remove_non_ascii(text):
    text = re.sub(r'[\357\254\200]+', 'ff', text)
    text = re.sub(r'[\357\254\201]+', 'fi', text)
    text = re.sub(r'[\357\254\202]+', 'fl', text)
    text = re.sub('fffi ', 'fi', text)
    text = re.sub('fff ', 'f', text)
    text = re.sub('ff ', 'ff', text)
    text = re.sub('-\n','', text)
    text = re.sub('[^0-9a-zA-Z]+', ' ', text)
    text = re.sub(r'[^\x00-\x7F]+',' ', text) 
    return(text)

#Eliminates some unimportant keywords, similarly to what is done in txt2key_phrases.py (l.75)
def merge_keywords(glob_files, glob_keyword, glob_keywords_file, importance):
    print(len(glob_keyword))
    print(glob_keyword)
    raw_input("Press the <ENTER> key to continue...")
    print(len(glob_files))
    list_zeros = [["" for n in xrange(len(glob_files)+3)] for _ in xrange(len(glob_keyword)+1)]
    for (y,f) in enumerate(glob_files):
        list_zeros[0][y+3]=f
        for (x,k) in enumerate(glob_keyword):
            list_zeros[x+1][0]=k
            if (f, k) in glob_keywords_file:
                list_zeros[x+1][y+3] = glob_keywords_file[(f,k)] 
            else:
                list_zeros[x+1][y+3] = 0
    final_list = []
    final_keywords = []
    for i in xrange(len(list_zeros)):
        imp = sum(1 for x in list_zeros[i] if x > 0.03)             # to be adjusted based on number of papers and user-s preferences
        if imp > importance:
            final_list.append(list_zeros[i])
            final_keywords.append(list_zeros[i][0])
    print(len(final_keywords))
    print(final_keywords)
    raw_input("Press the <ENTER> key to continue...")
    return([final_list, final_keywords])


#Writes the final list of keywords in the CSV file
def keywords2file(final_list, file_name):
    with open(file_name, 'w') as kw_output:
        w = csv.writer(kw_output)
        w.writerows(final_list)
    

#Calculates the frequency/occurenceimportance of keywords
def txt2tfidf(txt_dir, kw_out):
    """Execute RAKE and TF-IDF algorithms on each page and output top scoring phrases"""
    
    glob_keywords_file_TFIDF = {}
    glob_files_TFIDF = set()
    glob_keyword_TFIDF = set()
    start_time = time.time()

    #2: Collect raw text for pages
    print("=== 2. Collect Raw Text")
    processed_pages = []
    dir_files = txt_dir                                             #Location where the TXT files are
    processed_pages = []
    for f in glob.glob(dir_files + "/" + "*.txt"):                  #Loops over all the TXT files
        with open(f, 'r') as content_file:
            content = content_file.read()                           #Reads the files     
        processed_pages.append({"url": str(f), "text": remove_non_ascii(content)}) #Adds the name of the file to processed_pages, and the corresponding text from the TXT files
           
    #3: TF-IDF keywords for processed text
    print("=== 3. TF-IDF")
    document_frequencies = {}
    document_count = len(processed_pages)
    for page in processed_pages[1:document_count]:                                  #For all processed pages
        page["tfidf_frequencies"] = tfidf.get_word_frequencies(page["text"])        #Calculates the frequency of the wprd
        for word in page["tfidf_frequencies"]:                                      #Calculates the frequency of the word in a document
            document_frequencies.setdefault(word, 0)
            document_frequencies[word] += 1                                         #To avoid zeros


    sortby = lambda x: x[1]["score"]
    for page in processed_pages[1:document_count]:                                  # names page --> txt file
        for word in page["tfidf_frequencies"].items():
            word_frequency = word[1]["frequency"]
            docs_with_word = document_frequencies[word[0]]
            word[1]["score"] = tfidf.calculate(word_frequency, document_count, docs_with_word)

        page["tfidf_results"] = sorted(page["tfidf_frequencies"].items(), key=sortby, reverse=True)
        #The word is considered a keyword if its frequency is higher than 0.08 (parameter adjustment, needs to be computed rather than set by hand)
        short_keywords_tfidf = [k[0] for k in page["tfidf_results"] if k[1]["score"] > 0.08] 
        paper = page["url"]
    	short_kw_dict_tfidf = {(paper,k[0]):k[1]["score"] for k in page["tfidf_results"] if k[1]["score"] > 0.08} 
    	glob_keyword_TFIDF |= set(short_keywords_tfidf)
    	glob_files_TFIDF.add(paper)                                                                         
    	glob_keywords_file_TFIDF.update(short_kw_dict_tfidf)
    	#Makes the list of keywords       
    print("TF-IDF: %d" % (time.time() - start_time))

    
    file_tfidf = kw_out
    importance = int(math.sqrt(math.sqrt(len(processed_pages))))+1
    #Calculates the final list of important keywords based on the importance
    [final_TFIDF, final_keywords_TFIDF] = merge_keywords(glob_files_TFIDF, glob_keyword_TFIDF, glob_keywords_file_TFIDF, importance)

    j=0
    distance_matrix =  [[1000 for n in xrange(len(final_keywords_TFIDF))] for k in xrange(len(final_keywords_TFIDF))]
    db = DBSCAN(eps=0.02, min_samples=2, metric="precomputed")                  #Density-Based Spatial Clustering of Applications with Noise. eps=max distance to be considered as neighbour
    y_db = db.fit_predict(distance_matrix)                                      #Performs clustering on distance_matrix and returns cluster labels.

            
    #Sets categories and definitions of the keywords            
    for i in range(len(y_db)):
        if i > 0:
            ss = wn.synsets(final_TFIDF[i][0])
            categories = " "
            for s in ss[0].hypernym_paths()[0][3:-1]:
                categories =  categories + " " +s.name().split('.')[0] 
            final_TFIDF[i][1] = categories                                      #y_db[i-1]
            final_TFIDF[i][2] = ss[0].definition()                              #y_db[i-1]  
    keywords2file(final_TFIDF, file_tfidf)   
    end_time = time.time() - start_time
    print('Done. Elapsed: %d' % end_time)
        


#For an explanation of what tf-idf does and how, check this webpage: http://scikit-learn.org/stable/modules/feature_extraction.html#tfidf-term-weighting
