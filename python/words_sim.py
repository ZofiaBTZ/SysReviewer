import sys
import re
import urllib2
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

#todo - basic similarity, bags of words, bags of words combined with similarity --- to get synonyms
# co-occurences - to group into contexts; acronyms, 
# c
     
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic
brown_ic = wordnet_ic.ic('ic-brown.dat')
semcor_ic = wordnet_ic.ic('ic-semcor.dat')

from nltk.corpus import genesis
genesis_ic = wn.ic(genesis, False, 0.0)



word1 = sys.argv[1]
word2 = sys.argv[2]

def1 = word1 + '.n.01'
def2 = word2 + '.n.01'

sn1 = wn.synset(def1)
sn2 = wn.synset(def2)

print(sn1.definition())
print(sn2.definition())

print(sn1.hyponyms())
print(sn2.hyponyms())

print(sn1.hypernyms())
print(sn2.hypernyms())

print(sn1.examples())
print(sn2.examples())

def1 = sn1.definition()
def1_set = set(re.findall(r'\w+', def1))
def2 = sn2.definition()
def2_set = set(re.findall(r'\w+', def2))
u = set.intersection(def1_set, def2_set)
print(u)

sim_path = sn1.path_similarity(sn2)
sim_wup = sn1.wup_similarity(sn2)
sim_lch = sn1.lch_similarity(sn2)
res_brown = sn1.res_similarity(sn2, brown_ic)
res_semcor = sn1.res_similarity(sn2, semcor_ic)
res_genesis = sn1.res_similarity(sn2, genesis_ic)
#dog.jcn_similarity(cat, brown_ic) 
jcn_brown = sn1.jcn_similarity(sn2, brown_ic)
jcn_semcor = sn1.jcn_similarity(sn2, semcor_ic)
jcn_genesis = sn1.jcn_similarity(sn2, genesis_ic)

lin_brown = sn1.lin_similarity(sn2, brown_ic)
lin_semcor = sn1.lin_similarity(sn2, semcor_ic)
lin_genesis = sn1.lin_similarity(sn2, genesis_ic)


#pap1 = pap + word1
#pap2 = pap + word2
#pap12 = pap + word1 + " AND " + word2
#freq1 = pap2freq(pap1)
#print(freq1)
#freq2 = pap2freq(pap2)
#print(freq2)
#freq12 = pap2freq(pap12)
#print(freq12)
#simSym12 = all*freq12/(freq1 * freq2)
#sim12 = freq12/freq1
#sim21 = freq12/freq2

#print("Symmetric simmilarity = " + str(simSym12))
#print(word1 + " as subcategory of " + word2 + " " + str(sim12))
#print(word2 + " as subcategory of " + word1 + " " + str(sim21))

print(word1 + " and " + word2 + " path similarity is: " + str(sim_path))
print(word1 + " and " + word2 + " lch similarity is: " + str(sim_lch))
print(word1 + " and " + word2 + " wup similarity is: " + str(sim_wup))

print(word1 + " and " + word2 + " res brown similarity is: " + str(res_brown))
print(word1 + " and " + word2 + " res semcor similarity is: " + str(res_semcor))
print(word1 + " and " + word2 + " res genesis similarity is: " + str(res_genesis))

print(word1 + " and " + word2 + " jcn brown similarity is: " + str(jcn_brown))
print(word1 + " and " + word2 + " jcn semcor similarity is: " + str(jcn_semcor))
print(word1 + " and " + word2 + " jcn genesis similarity is: " + str(jcn_genesis))
print(word1 + " and " + word2 + " lin brown similarity is: " + str(lin_brown))
print(word1 + " and " + word2 + " lin semcor similarity is: " + str(lin_semcor))
print(word1 + " and " + word2 + " lin genesis similarity is: " + str(lin_genesis))




