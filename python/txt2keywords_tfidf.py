"""Script to run through new cleanse and RAKE logic"""
import os
import time
import requests
from bs4 import BeautifulSoup
#import contentloader
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
#from short_similarity_sujipal import word_similarity
import math
#from domains import * 

#import textrank

#RAKE_STOPLIST = './Malawi_search_words/stopwords_long_tfidf.txt'
CACHE_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'cache')


subset = 500


def remove_non_ascii(text):
    text = re.sub(r'[\357\254\200]+', 'ff', text)
    text = re.sub(r'[\357\254\201]+', 'fi', text)
    text = re.sub(r'[\357\254\202]+', 'fl', text)
    text = re.sub('fffi ', 'fi', text)
    text = re.sub('fff ', 'f', text)
    text = re.sub('ff ', 'ff', text)
    text = re.sub('-\n','', text)
    text = re.sub('[^0-9a-zA-Z]+', ' ', text)
 #   text = re.sub(r'[^\x00-\x7F]+',' ', text) 
    return(text)


def merge_keywords(glob_files, glob_keyword, glob_keywords_file, importance):
    print(len(glob_keyword))
    print(len(glob_files))
    list_zeros = [["" for n in xrange(len(glob_files)+3)] for _ in xrange(len(glob_keyword)+1)]
    for (y,f) in enumerate(glob_files):
        list_zeros[0][y+2]=f
        for (x,k) in enumerate(glob_keyword):
            list_zeros[x+1][0]=k
            if (f, k) in glob_keywords_file:
                list_zeros[x+1][y+2] = glob_keywords_file[(f,k)] 
                #print(glob_keywords_file[(f,k)])
            else:
                list_zeros[x+1][y+2] = 0
            
    final_list = []
    final_keywords = []
    for i in xrange(len(list_zeros)):
        imp = sum(1 for x in list_zeros[i] if x > 0.03) # to be adjusted based on number of papers and user-s preferences
        if imp > importance:
            final_list.append(list_zeros[i])
            final_keywords.append(list_zeros[i][0])
    return([final_list, final_keywords])

def keywords2file(final_list, file_name):
    with open(file_name, 'w') as kw_output:
        w = csv.writer(kw_output)
        w.writerows(final_list)
    

def txt2tfidf(txt_dir, kw_out):
    """Execute RAKE and TF-IDF algorithms on each page and output top scoring phrases"""
    #glob_keywords_file_RAKE = {}
    #glob_files_RAKE = set()
    #glob_keyword_RAKE = set()
    
    glob_keywords_file_TFIDF = {}
    glob_files_TFIDF = set()
    glob_keyword_TFIDF = set()
    start_time = time.time()

    #2: Collect raw text for pages
    print("=== 2. Collect Raw Text")
    processed_pages = []
    dir_files = txt_dir #"./output_legionella_txt/"
    processed_pages = []
    for f in glob.glob(dir_files + "/" + "*.txt"):
        with open(f, 'r') as content_file:
            content = content_file.read()
            
        processed_pages.append({"url": str(f), "text": remove_non_ascii(content)}) # change naming url -- > txt file
           
    #3: TF-IDF keywords for processed text
    print("=== 3. TF-IDF")
    document_frequencies = {}
    document_count = subset#len(processed_pages)
    for page in processed_pages[1:subset]:
        page["tfidf_frequencies"] = tfidf.get_word_frequencies(page["text"])
        for word in page["tfidf_frequencies"]:
            document_frequencies.setdefault(word, 0)
            document_frequencies[word] += 1
            #print(word)

    sortby = lambda x: x[1]["score"]
    for page in processed_pages[1:subset]: # names page --> txt file
        for word in page["tfidf_frequencies"].items():
            word_frequency = word[1]["frequency"]
            #print word[0] + " " + str(word_frequency)
            docs_with_word = document_frequencies[word[0]]
            word[1]["score"] = tfidf.calculate(word_frequency, document_count, docs_with_word)

        page["tfidf_results"] = sorted(page["tfidf_frequencies"].items(), key=sortby, reverse=True)
        short_keywords_tfidf = [k[0] for k in page["tfidf_results"] if k[1]["score"] > 0.08] # adjust the parameters 
        paper = page["url"]
    	short_kw_dict_tfidf = {(paper,k[0]):k[1]["score"] for k in page["tfidf_results"] if k[1]["score"] > 0.08}
    	glob_keyword_TFIDF |= set(short_keywords_tfidf)
    	glob_files_TFIDF.add(paper)
    	glob_keywords_file_TFIDF.update(short_kw_dict_tfidf)
        
    print("TF-IDF: %d" % (time.time() - start_time))

    #5. TextRank
   # print("=== 5. TextRank")
   # for page in processed_pages:
   #     textrank_results = textrank.extractKeyphrases(page["text"])
   #     page["textrank_results"] = sorted(textrank_results.items(), key=lambda x: #x[1], reverse=True)
   # print("TextRank: %d" % (time.time() - start_time))

    #6. Results
    #print("=== 6. Results")
    #for page in processed_pages:
    #    print("-------------------------")
    #    print("URL: %s" % page["url"])
    #    print("RAKE:")
    #    for result in page["rake_results"][:45]:
    #        print(" * %s" % result[0])
    #    print("TF-IDF:")
    #    for result in page["tfidf_results"][:45]:
    #        print(" * %s" % result[0])
    #    print("TextRank:")
    #    for result in page["textrank_results"][:5]:
    #        print(" * %s" % result[0])

    
    file_tfidf = kw_out#sys.argv[1]
    #file_rake = sys.argv[2]
    [final_TFIDF, final_keywords_TFIDF] = merge_keywords(glob_files_TFIDF, glob_keyword_TFIDF, glob_keywords_file_TFIDF, 3)
#    [final_RAKE, final_keywords_RAKE] = merge_keywords(glob_files_RAKE, glob_keyword_RAKE, glob_keywords_file_RAKE, 3)

    
  #  table_keywords = [(k1,k2) for k1 in final_keywords for k2 in final_keywords_TFIDF] 
    #distance_matrix = [(k1,k2, similarity(k1,k2, True)) for (k1,k2) in table_keywords]
    j=0
    distance_matrix =  [[1000 for n in xrange(len(final_keywords_TFIDF))] for k in xrange(len(final_keywords_TFIDF))]
    #for i in xrange(1,len(final_keywords_TFIDF)):
    #    for j in xrange(i+1,len(final_keywords_TFIDF)-1):
    #        #     print(final_keywords_TFIDF[i])
    #        w_sim = word_similarity(final_keywords_TFIDF[i], final_keywords_TFIDF[j])
    #        w_sim2 = word_similarity(final_keywords_TFIDF[j], final_keywords_TFIDF[i])
    #        distance_matrix[i][j] = (1/(0.000001 + w_sim*w_sim*w_sim*w_sim))/100
    #        distance_matrix[j][i] = (1/(0.000001 + w_sim2*w_sim2*w_sim2*w_sim2))/100
            #if distance_matrix[i][j] < 0.4:
             #   print(final_keywords_TFIDF[i] + " " + final_keywords_TFIDF[j] + " " + str(distance_matrix[i][j]))# +str(distance_matrix[j][i]) )
            #    print(distance_matrix)

    #hcl.linkage(squareform(distance_matrix))
 # clean it !!!
    db = DBSCAN(eps=0.02, min_samples=2, metric="precomputed")
    y_db = db.fit_predict(distance_matrix)
    #print(len(final_keywords))

    #domain2synsets = defaultdict(list)
    #synset2domains = defaultdict(list)
    #for i in open('wn_domains.txt', 'r'):
    #    tmp = i.strip().split('\t')
    #    if len(tmp)>1:
    #        ssid = tmp[0]
    #        doms = tmp[1]
    #        doms = doms.split()
    #        synset2domains[ssid] = doms
    #        for d in doms:
    #            domain2synsets[d].append(ssid)
            
                
    for i in range(len(y_db)):
        if i > 0:
            ss = wn.synsets(final_TFIDF[i][0])
            categories = " "
            for s in ss[0].hypernym_paths()[0][3:-1]:
                categories =  categories + " " +s.name().split('.')[0] 

            final_TFIDF[i][1] = categories#y_db[i-1]
            final_TFIDF[i][2] = ss[0].definition()#y_db[i-1]
  
    keywords2file(final_TFIDF, file_tfidf)
#    keywords2file(final_RAKE, file_rake)
    #    file_RAKE = sys.argv[2]
    #    final_RAKE = merge_keywords(glob_files_RAKE, glob_keyword_RAKE, glob_keywords_file_RAKE, 6)
    #    keywords2file(final_RAKE, file_RAKE)

    end_time = time.time() - start_time
    print('Done. Elapsed: %d' % end_time)
        
# txt2tfidf(txt_dir, kw_out)


