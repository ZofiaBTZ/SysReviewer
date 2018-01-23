#Imports
import sys
import re
import numpy as np
import pandas as pd
import time
import csv

from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic
brown_ic = wordnet_ic.ic('ic-brown.dat')
semcor_ic = wordnet_ic.ic('ic-semcor.dat')

from nltk.corpus import genesis
genesis_ic = wn.ic(genesis, False, 0.0)


#Creates keywords list from formed CSV file with sysReview.py
def create_list(keywords_file):
    with open(keywords_file, 'rb') as csvfile:
        data_CSV = csv.reader(csvfile, delimiter=',')
        words, path, definition = [], [], []
        for row in data_CSV:
            words.append(row[0])
            path.append(row[1])
            definition.append(row[2])
            all = len(row)-2
        words = filter(None, words)                                 #Removes empty items in list
        path = filter(None, path)
        definition = filter(None, definition)
    return (words, all)

#Calculates frequencies of words
def calc_freq(keywords_file, freq_words, words):
    #Sets the tables of indexes
    with open(keywords_file, 'rb') as csvfile:
        data_CSV = csv.reader(csvfile, delimiter=',')
        which_paper, kw_nber = [], []
        for row in data_CSV:                                        #Loops on the rows of the CSV File
            for col in row:                                         #Loops on the columns of one row of the CSV File
                if ('0.' in col) and not ('.txt' in col):           #If there is something with '0.' in the element, which is not in the filename, then the keyword corresponding to row has an occurence
                    which_paper.append(row.index(col))              #We check in which paper this is
                    kw_nber.append(data_CSV.line_num - 2)           #And which corresponding keyword of index kw_nber in words
    #initialises first row/column
    for w1 in xrange(len(words)):
        freq_words[w1+1][0] = words[w1]                             #Store the word in the first line
        freq_words[0][w1+1] = words[w1]
    #Calculates the frequencies          
    for pap in xrange(len(which_paper)):
        for pap2 in xrange(len(which_paper)):
            if (which_paper[pap] == which_paper[pap2]):             #if two words in the same paper, then increase frequency by 1
                freq_words[int(kw_nber[pap])+1][int(kw_nber[pap2])+1] += 1.
    return   

#Calculates the cooccurence 
def words_cooccurence(keywords_file):
    #To set the list of words
    words, all = create_list(keywords_file)
    #Sets all matrice objects to 0
    freq_words =  [[0. for x in xrange(len(words)+1)] for y in range(len(words) +1)]         
    symSim =  [[0. for x in xrange(len(words)+1)] for y in range(len(words) +1)]
    sim12 =  [[0. for x in xrange(len(words)+1)] for y in range(len(words) +1)]
    sim21 =  [[0. for x in xrange(len(words)+1)] for y in range(len(words) +1)]
    #Calculate freq_words
    calc_freq(keywords_file, freq_words, words)
    #Stores raw frequencies
    df_freq = pd.DataFrame(freq_words)                              
    df_freq.to_csv("CSV/frequencies.csv", sep=',')
    #Calculates sims    
    for w1 in xrange(len(words)):
        sim12[w1+1][0] = words[w1]					
        sim12[0][w1+1] = words[w1]					
        symSim[w1+1][0] = words[w1]					
        symSim[0][w1+1] = words[w1]
        for w2 in xrange(len(words)):
            sim12[w1+1][w2+1] = freq_words[w1+1][w2+1]/(freq_words[w1+1][w1+1]+1)	    #sim12 = 1 in diagonals (construction); = #of papers with word w1 AND w2/#of papers with word w1         
            symSim[w1+1][w2+1] = all*sim12[w1+1][w2+1]/(freq_words[w2+1][w2+1]+1)           #symSim = sim12/#of paper with word w2 * all papers == cooccurence?

    #Stores sims
    df_sim = pd.DataFrame(sim12)
    df_sim.to_csv("CSV/AsymSim.csv", sep=',')

    df_Symsim = pd.DataFrame(symSim)
    df_Symsim.to_csv("CSV/SymSim.csv", sep=',')                             #Triangular matrix. If not, there is a problem!
    return






