import sys
import re
import urllib2
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from words_cooccurence_downloaded import create_list
import os
import errno

#todo - basic similarity, bags of words, bags of words combined with similarity --- to get synonyms
# co-occurences - to group into contexts; acronyms
     
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic
brown_ic = wordnet_ic.ic('ic-brown.dat')
semcor_ic = wordnet_ic.ic('ic-semcor.dat')

from nltk.corpus import genesis
genesis_ic = wn.ic(genesis, False, 0.0)



def pap2freq(my_url):
    r = requests.get(my_url)                                                            #Calls the webpage
    soup_all = BeautifulSoup(r.content, "html.parser")					#Return the HTML source code in soup_all
    freq_div = soup_all.find("div", {"class":"text-muted"})	                        #Looks for a "div" tag with a "text-muted" class in the HTML code 			
    try:
        freq = freq_div.getText()	                                                #Gets the text of the HTML page without the code/tags...						
        str_freq = str(freq).split()[0]                                                 #Cuts the sentence stored in freq in separate words and keeps the first one (#of papers found with the search terms)
        str_freq = ''.join(str_freq.split(','))                                         #If there are more tham 1000 matches, then removes the  OR  character for getting a number
        #print ("str_freq 1", str_freq)                                                  #str_freq is the number of papers found with the search terms, in string format
    except:
        time.sleep(10)                                                                  
        try:
            r = requests.get(my_url)
            soup_all = BeautifulSoup(r.content, "html.parser")                          
            freq_div = soup_all.find("div", {"class":"text-muted"})                     
            freq = freq_div.getText()                                                   
            str_freq = str(freq).split()[0]                                             
            str_freq = ''.join(str_freq.split(','))                                                                        
        except:
            str_freq = -1
            return str_freq
    return((str_freq))
 
def words_cooccurence_paperity_f(keywords_file, output_name):

    try:
        os.makedirs(output_name + "/CSV/")
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
        
    words, all = create_list(keywords_file)
    pap = "http://paperity.org/search/?q="

##    all = float(pap2freq(pap))                                                              #Gets the total number of papers in paperity.org
##    #Keywords list
##    words = ["tobacco", "palliative", "music", "ocimum", "democracy", "tradition", "populism", "pentecostalism",
##         "god", "tiu", "urd", "witchcraft", "misconception", "mathematics", "pathology" ,"pharmacy", "pediatrics", 
##         "midwifery", "psychiatry", "gender", "violence", "abortion", "vaccine", "injection",
##         "job", "adoption", "PMTCT", "prevention of mother to child transmission", "prevention of mother-to-child transmission"]
##    words =  ["sex", "HIV", "AIDS", "stigma", "condom", "witchcraft", "misconception OR diarrhea" , "diarrhoea", "PMTCT", "prevention of mother to child transmission", "mother", "abortion", "vaccine", "injection", "drug", "pediatrics", "violence",
##          "cash transfer", "tobacco", "malaria", "p-value", "PCA", "zidovudine", "antiretroviral drugs" ,"ARV",
##          "initiated ART", "HIV treatment", "ART", "HIV prevention", "high risk sex", "overweight", "nutrition",
##          "malnutrition", "WAZ", "HAZ", "food security", "pregnant and lactating woman", "pregnancy outcomes",
##          "postpartum period", "postnatal care", "perinatal mortality", "ANC clinic", "categorical variables", 
##          "bivariate analysis", "binary variables OR ANOVA", "sex work", "Transactional sex", "knowledge gap",
##          "isolation", "involvement", "intimate partner violence", "incentives", "human rights OR freedom",
##          "enabling environment", "MSM", "Malawi", "banja la mtsogolo", "adult patients", "visits", "utilization",
##          "transport", "visit", "road", "registration", "personal identifiers", "nearest health facility",
##          "long waiting times", "long distance", "inability", "home visits", "health passport",
##          "clinic visit", "catchment", "barriers", "attendance", "appointment", "contraceptive decision making",
##          "development programmes", "tb diagnosis", "hiv counselling", "social safety net", "good practice",
##          "water development", "ethnic groups", "hiv aids epidemic", "structural violence", "poor rural setting",
##          "generalized hiv epidemics", "health providers", "household expenditures", "district health services",
##          "executive committee", "accepting hiv testing", "delivering antiretroviral therapy", "popular culture",
##          "water points", "resource poor country", "health center level", "adult literacy",
##          "medical doctors", "middle class", "social desirability", "desired family size", "sexual risks",
##          "natural resources management", "poor working conditions", "blantyre malawi", "risk factors",
##          "antiretroviral therapy programme", "arable land", "infectious diseases", "high proportion", 
##          "average age", "lower level", "hiv status", "african systems", "negotiate safe sex", "development economics",
##          "policy changes", "presents summary statistics", "hiv virus", "rural adults", "social factors", "john stewart",
##          "public domain", "expenditure patterns", "men women", "extension workers", "increase hiv testing",
##          "clinical data", "minimum level", "survey round", "general health care", "educational status",
##          "national sample survey", "balaka district", "positive effects", "health seeking behaviour",
##          "decision making", "international aid", "public works", "poor evidence", "housing quality", 
##          "family members friends", "malawian ministry", "urban residence"]    
##    words =  ["HIV OR sex OR AIDS OR Malawi OR condom OR stigma OR antiretroviral OR virus OR HIV testing",
##              "sexual risks OR safe sex OR epidemics OR prevention OR PCA OR contraception OR high risk sex",
##              "treatment OR knowledge gap OR intimate partner violence OR clinic visit OR counselling OR risk factors",
##             "tb diagnosis OR HIV status OR therapy OR social factors OR health seeking behaviour"]


    #Set all matrices objects to 0
    freq_words =  [[0 for x in xrange(len(words)+1)] for y in range(len(words) +1)]         
    symSim =  [[0 for x in xrange(len(words)+1)] for y in range(len(words) +1)]
    sim12 =  [[0 for x in xrange(len(words)+1)] for y in range(len(words) +1)]
    sim21 =  [[0 for x in xrange(len(words)+1)] for y in range(len(words) +1)]


    for w1 in xrange(len(words)):
        freq_words[w1+1][0] = words[w1]                             #Store the word in the first line
        freq_words[0][w1+1] = words[w1]                             #Store the word in the first column
        for w2 in xrange(len(words)):
            if (w1==w2):                                            #If the two indexes w1,w2 are equal, the search is run only with one keyword
                my_url = pap + "\"" + words[w1] + "\""
            else:                                                   #Else, with both associated keywords
                my_url = pap + "\"" + words[min(w1,w2)] + "\"" + " AND " + "\"" + words[max(w1,w2)] + "\""
            freq_words[w1+1][w2+1] = float(pap2freq(my_url))

        
    df_freq = pd.DataFrame(freq_words)                              #Store this matrix to a CSV file
    df_freq.to_csv(output_name + "/CSV/frequencies_"+keywords_file[-17:-15]+"pap.csv", sep=',')


    for w1 in xrange(len(words)):
        sim12[w1+1][0] = words[w1]					
        sim12[0][w1+1] = words[w1]					
        symSim[w1+1][0] = words[w1]					
        symSim[0][w1+1] = words[w1]
        for w2 in xrange(len(words)):
            sim12[w1+1][w2+1] = freq_words[w1+1][w2+1]/(freq_words[w1+1][w1+1]+1)		      #sim12 = 1 in diagonals (construction); = #of papers with word w1 AND w2/#of papers with word w1         
            symSim[w1+1][w2+1] = all*sim12[w1+1][w2+1]/(freq_words[w2+1][w2+1]+1)                   #symSim = sim12/#of paper with word w2 * all papers == cooccurence?


    df_sim = pd.DataFrame(sim12)
    df_sim.to_csv(output_name + "/CSV/AsymSim_"+keywords_file[-17:-15]+"pap.csv", sep=',')

    df_Symsim = pd.DataFrame(symSim)
    df_Symsim.to_csv(output_name + "/CSV/SymSim_"+keywords_file[-17:-15]+"pap.csv", sep=',')                                                         #Triangular matrix. If not, there is a problem!







