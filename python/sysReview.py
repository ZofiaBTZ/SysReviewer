from paperity2pdf import parse
from pdf2txt import convert
from txt2key_phrases import txt2keyphrases
from txt2keywords_tfidf import txt2tfidf
from txt2textRank import txt2textRank
from sysReview_searchpaperity import args2query
from words_cooccurence_downloaded import words_cooccurence
from words_cooccurence_paperity import words_cooccurence_paperity_f
import os, errno
import sys


parsed = args2query()
query = parsed["query"]                             #query = search terms
output_name = parsed["output_name"]
print("query", query)
print("output_name", output_name)

try:
    os.makedirs("../../Output/")
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
     
output_name = "../../Output/" + output_name
print(output_name)
output_pdf = output_name + "/output_pdf"             
output_txt = output_name + "/output_txt"             
summary_file = output_name + "/summary_file.txt"      
keyphrases_file = output_name + "/kp_prake_file.csv"                 
keywords_file = output_name + "/kw_tfidf_file.csv"  
textRank_file = output_name + "/kp_textRank_file_.csv"   
last_page = 1                                                          #Put that to 1 if it's a new search
#print("Downloading papers...")
#parse(query, output_pdf, last_page)                                     #paperity2pdf, downloads paperity papers
#print("Converting downloaded papers")
#convert(output_pdf, output_txt, summary_file)                           #pdf2txt, transforms downloaded papers in txt
#print("Extractiong keyphrases")
#txt2keyphrases(output_txt, keyphrases_file)                             #txt2key_phrases
#print("Extracting keywords")
#txt2tfidf(output_txt, keywords_file)                                    #txt2keywords_tfidf
txt2textRank(output_txt, textRank_file, output_name)
print("Cooccurrence in downloaded papers for keyphrases")
words_cooccurence(textRank_file, output_name)                         #words_cooccurence_downloaded
#print("Cooccurrence in downloaded papers for keywords")
#words_cooccurence(keywords_file, output_name)                           #words_cooccurence_downloaded
#print("Cooccurrence in paperity for keyphrases")
#words_cooccurence_paperity_f(keyphrases_file, output_name)              #words_cooccurence_paperity
#print("Cooccurrence in paperity for keywords")
#words_cooccurence_paperity_f(keywords_file, output_name)                #words_cooccurence_paperity


#python sysReview.py --author "" --keywords "HIV OR sex OR AIDS OR Malawi OR condom OR stigma OR antiretroviral OR virus OR HIV testing OR sexual risks OR safe sex OR epidemics OR prevention OR PCA OR contraception OR high risk sex OR treatment OR knowledge gap OR intimate partner violence OR clinic visit OR counselling OR risk factors OR tb diagnosis OR HIV status OR therapy OR social factors OR health seeking behaviour"
#How to use example: python sysReview.py --author "Olivia AND Keiser" --keywords "HIV in Malawi"
#Author AND keywords are BOTH mandatory
#Careful, if the query is too big, the name of the output directory/files will be too long and python won't be able to create it
