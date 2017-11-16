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



def pap2freq(my_url):
    r = requests.get(my_url)
    #print(r.content)
    soup_all = BeautifulSoup(r.content, "html.parser")
    freq_div = soup_all.find("div", {"class":"text-muted"})
    try:
        freq = freq_div.getText()
        print(freq)
        str_freq = str(freq).split()[0]
        str_freq = ''.join(str_freq.split(','))
    except:
        time.sleep(10)
        try:
            r = requests.get(my_url)
            soup_all = BeautifulSoup(r.content, "html.parser")
            freq_div = soup_all.find("div", {"class":"text-muted"})
            freq = freq_div.getText()
            print(freq)
            str_freq = str(freq).split()[0]
            str_freq = ''.join(str_freq.split(','))
        except:
            str_freq = -1
            return str_freq
    return((str_freq))


def cache2papFreq(my_url):
    url_hash = str(hash(my_url))
    try:
        f = file('./tmp/cache/a'+ url_hash)
        if (f.read != -1):
            return float(f.read())
    except:
        print("look online " + my_url)
        time.sleep(3)
        
    freq = pap2freq(my_url)
    f = file('./tmp/cache/a'+ url_hash, 'w')
    f.write(freq)
   
    return float(freq)


all = 1200000

pap = "http://paperity.org/search/?q="
words = ["tobacco", "palliative", "music", "ocimum", "democracy", "tradition", "populism", "pentecostalism",
         "god", "tiu", "urd", "witchcraft", "misconception", "mathematics", "pathology" ,"pharmacy", "pediatrics", 
         "midwifery", "psychiatry", "gender", "violence", "abortion", "vaccine", "injection",
         "job", "adoption", "PMTCT", "prevention of mother to child transmission", "prevention of mother-to-child transmission"]

words =  ["sex", "HIV", "AIDS", "stigma", "condom", "witchcraft", "misconception","diarrhea" , "diarrhoea", "PMTCT", "prevention of mother to child transmission", "mother", "abortion", "vaccine", "injection", "drug", "pediatrics", "violence",
          "cash transfer", "tobacco", "malaria", "p-value", "PCA", "zidovudine", "antiretroviral drugs" ,"ARV",
          "initiated ART", "HIV treatment", "ART", "HIV prevention", "high risk sex", "overweight", "nutrition",
          "malnutrition", "WAZ", "HAZ", "food security", "pregnant and lactating woman", "pregnancy outcomes",
          "postpartum period", "postnatal care", "perinatal mortality", "ANC clinic", "categorical variables", 
          "bivariate analysis", "binary variables","ANOVA", "sex work", "Transactional sex", "knowledge gap",
          "isolation", "involvement", "intimate partner violence", "incentives", "human rights","freedom",
          "enabling environment", "MSM", "Malawi", "banja la mtsogolo", "adult patients", "visits", "utilization",
          "transport", "visit", "road", "registration", "personal identifiers", "nearest health facility",
          "long waiting times", "long distance", "inability", "home visits", "health passport",
          "clinic visit", "catchment", "barriers", "attendance", "appointment", "contraceptive decision making",
          "development programmes", "tb diagnosis", "hiv counselling", "social safety net", "good practice",
          "water development", "ethnic groups", "hiv aids epidemic", "structural violence", "poor rural setting",
          "generalized hiv epidemics", "health providers", "household expenditures", "district health services",
          "executive committee", "accepting hiv testing", "delivering antiretroviral therapy", "popular culture",
          "water points", "resource poor country", "health center level", "adult literacy",
          "medical doctors", "middle class", "social desirability", "desired family size", "sexual risks",
          "natural resources management", "poor working conditions", "blantyre malawi", "risk factors",
          "antiretroviral therapy programme", "arable land", "infectious diseases", "high proportion", 
          "average age", "lower level", "hiv status", "african systems", "negotiate safe sex", "development economics",
          "policy changes", "presents summary statistics", "hiv virus", "rural adults", "social factors", "john stewart",
          "public domain", "expenditure patterns", "men women", "extension workers", "increase hiv testing",
          "clinical data", "minimum level", "survey round", "general health care", "educational status",
          "national sample survey", "balaka district", "positive effects", "health seeking behaviour",
          "decision making", "international aid", "public works", "poor evidence", "housing quality", 
          "family members friends", "malawian ministry", "urban residence"] 

freq_words =  [[0 for x in xrange(len(words)+1)] for y in range(len(words) +1)]
symSim =  [[0 for x in xrange(len(words)+1)] for y in range(len(words) +1)]
sim12 =  [[0 for x in xrange(len(words)+1)] for y in range(len(words) +1)]
sim21 =  [[0 for x in xrange(len(words)+1)] for y in range(len(words) +1)]


for w1 in xrange(len(words)):
    freq_words[w1+1][0] = words[w1]
    freq_words[0][w1+1] = words[w1]
    for w2 in xrange(len(words)):
        if (w1==w2):
            my_url = pap + "\"" + words[w1] + "\""
        else:
            my_url = pap + "\"" + words[min(w1,w2)] + "\"" + " AND " + "\"" + words[max(w1,w2)] + "\""
        freq_words[w1+1][w2+1] = cache2papFreq(my_url) 
        
df_freq = pd.DataFrame(freq_words)
df_freq.to_csv("frequencies.csv", sep=',')

for w1 in xrange(len(words)):
    sim12[w1+1][0] = words[w1]
    sim12[0][w1+1] = words[w1]
 #   sim21[w1+1][0] = words[w1]
 #   sim21[0][w1+1] = words[w1]
    symSim[w1+1][0] = words[w1]
    symSim[0][w1+1] = words[w1]
    for w2 in xrange(len(words)):
        sim12[w1+1][w2+1] = freq_words[w1+1][w2+1]/(freq_words[w1+1][w1+1]+1)        
#        sim21[w1+1][w2+1] = freq_words[w1+1][w2+1]/freq_words[w2+1][w2+1] 
        symSim[w1+1][w2+1] = all*sim12[w1+1][w2+1]/(freq_words[w2+1][w2+1]+1) 

df_sim = pd.DataFrame(sim12)
df_sim.to_csv("AsymSim.csv", sep=',')

df_Symsim = pd.DataFrame(symSim)
df_Symsim.to_csv("SymSim.csv", sep=',')



#word1 = sys.argv[1]
#word2 = sys.argv[2]

#def1 = word1 + '.n.01'
#def2 = word2 + '.n.01'

#sn1 = wn.synset(def1)
#sn2 = wn.synset(def2)

#print(sn1.definition())
#print(sn2.definition())

#print(sn1.hyponyms())
#print(sn2.hyponyms())

#print(sn1.hypernyms())
#print(sn2.hypernyms())

#print(sn1.examples())
#print(sn2.examples())

#def1 = sn1.definition()
#def1_set = set(re.findall(r'\w+', def1))
#def2 = sn2.definition()
#def2_set = set(re.findall(r'\w+', def2))
#u = set.intersection(def1_set, def2_set)
#print(u)

#sim_path = sn1.path_similarity(sn2)
#sim_wup = sn1.wup_similarity(sn2)
#sim_lch = sn1.lch_similarity(sn2)
#res_brown = sn1.res_similarity(sn2, brown_ic)
#res_semcor = sn1.res_similarity(sn2, semcor_ic)
#res_genesis = sn1.res_similarity(sn2, genesis_ic)
#dog.jcn_similarity(cat, brown_ic) 
#jcn_brown = sn1.jcn_similarity(sn2, brown_ic)
#jcn_semcor = sn1.jcn_similarity(sn2, semcor_ic)
#jcn_genesis = sn1.jcn_similarity(sn2, genesis_ic)

#lin_brown = sn1.lin_similarity(sn2, brown_ic)
#lin_semcor = sn1.lin_similarity(sn2, semcor_ic)
#lin_genesis = sn1.lin_similarity(sn2, genesis_ic)


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

#print(word1 + " and " + word2 + " path similarity is: " + str(sim_path))
#print(word1 + " and " + word2 + " lch similarity is: " + str(sim_lch))
#print(word1 + " and " + word2 + " wup similarity is: " + str(sim_wup))

#print(word1 + " and " + word2 + " res brown similarity is: " + str(res_brown))
#print(word1 + " and " + word2 + " res semcor similarity is: " + str(res_semcor))
#print(word1 + " and " + word2 + " res genesis similarity is: " + str(res_genesis))

#print(word1 + " and " + word2 + " jcn brown similarity is: " + str(jcn_brown))
#print(word1 + " and " + word2 + " jcn semcor similarity is: " + str(jcn_semcor))
#print(word1 + " and " + word2 + " jcn genesis similarity is: " + str(jcn_genesis))

#print(word1 + " and " + word2 + " lin brown similarity is: " + str(lin_brown))
#print(word1 + " and " + word2 + " lin semcor similarity is: " + str(lin_semcor))
#print(word1 + " and " + word2 + " lin genesis similarity is: " + str(lin_genesis))




