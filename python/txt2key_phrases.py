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
import RAKE

#Removes non ASCII characters
def remove_non_ascii(text):
    text = re.sub(r'[\357\254\200]+', 'ff', text)
    text = re.sub(r'[\357\254\201]+', 'fi', text)
    text = re.sub(r'[\357\254\202]+', 'fl', text)
    text = re.sub('fffi ', 'fi', text)
    text = re.sub('fff ', 'f', text)
    text = re.sub('fff', 'f', text)
    text = re.sub('-\n','', text)
    text = re.sub('[^0-9a-zA-Z]+', ' ', text)
    text = re.sub(r'[^\x00-\x7F]+',' ', text) 
    return(text)

#Unused functions
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

#Txt2keyphrases - Extracts keyphrases from txt-converted pdfs
def txt2keyphrases(txt_dir, kw_file):
    ro = RAKE.Rake("./stopwords_long.txt")                      #Sets a list of stop words, and tells RAKE to process all text with no constraints
    glob_keywords_file = {}
    glob_files = set()
    glob_keyword = set()
    freq =  5                                                  #Change this if memory error (too many keyphrases)
    length = 4
    n_file=0
    for f in glob.glob(txt_dir + "/" + "*.txt"):                #Loops on all the TXT files in the TXT directory
        with open(f, 'r') as content_file:                      #Reads the file
            content = content_file.read()
        n_file = n_file+1                                       #Increases #of files
        print(n_file)
        content = remove_non_ascii(content)                     #Removes non ASCII characters
        content = " ".join(content.split())                     #Then splits the words, and rejoin them 
        mytext = " ".join(content.split())
        keywords = ro.run(mytext)                               #Use RAKE to create the keyword/phrases
        print(f)
        short_keywords = [k for (k,v) in keywords if len(k.split()) > 0 and v > freq and len(k.split())<length]             #Only keeps words with more frequencies than freq and smaller than length 
        paper = os.path.basename(f)
        short_kw_dict = {(paper,k):v for (k,v) in keywords if len(k.split())>0  and v > freq and len(k.split())<length}     #Makes a dictionary of which papers have which phrases and with which frequency
        glob_keyword |= set(short_keywords)
        glob_files.add(os.path.basename(paper))                 #Adds to the list of files processed files                                                                          
        glob_keywords_file.update(short_kw_dict)                #Updates the dictionnary of keywords 

    
    print(len(glob_keyword))                                    #Amount of keyphrases
    print(len(glob_files))                                      #Amount of files

    list_zeros = [["" for n in xrange(len(glob_files)+3)] for _ in xrange(len(glob_keyword)+1)]
    for (y,f) in enumerate(glob_files):                             #Automatic counter with number of files
        list_zeros[0][y+2]=f                                        #In the first row, stores the filename, with a shift of 2
        for (x,k) in enumerate(glob_keyword):                       #Same for number of keyphrases
            list_zeros[x+1][0]=k                                    #In the first column, stores the keyphrase, with a shift of 1 to not interfere with the name of files in the first raw
            if (f, k) in glob_keywords_file:                        #If the keyword is present in file f, then stores the frequency for that row,column
                list_zeros[x+1][y+2] = glob_keywords_file[(f,k)] 
            else:                                                   #Otherwise, sets to 0
                list_zeros[x+1][y+2] = 0
 
    final_list = []
    final_keywords = []
    freq_papers = int(math.sqrt(math.sqrt(n_file)))+2               #Minimum amount of papers the keyphrases needs to be in to be classified as important             
    for n_row in xrange(len(list_zeros)):
        importance = sum(1 for x in list_zeros[n_row] if x > 0)     #Calculated the number of papers in which the keyphrase is.
        if importance > freq_papers:                                #If superior to the minimum, then the keyphrase is kept
            final_list.append(list_zeros[n_row])
            final_keywords.append(list_zeros[n_row][0])

    with open(kw_file, 'w') as kw_output:                           #wirtes the CSV file of final results
        w = csv.writer(kw_output)
        w.writerows(final_list)
        
