from paperity2pdf import parse
from pdf2txt import convert
from txt2key_phrases import txt2keyphrases
import os, errno
import sys
import argparse



parser = argparse.ArgumentParser(add_help=True)

parser.add_argument('--date', '-d', action="store", dest = "pubDate")
parser.add_argument('--author', '-a', action="store", dest= "author")
parser.add_argument('--keywords', '-k', action="store", dest="keyW")
#parser.add_argument('--databases', '-db', action="store", default = "all", dest="dataBases")

print parser.parse_args()
args = parser.parse_args()
print args.pubDate
print args.author
print args.keyW

#https://www.ncbi.nlm.nih.gov/pmc/?term=(((Keiser,+Olivia%5BAuthor%5D)+AND+HIV%5BAbstract%5D)+AND+Malawi%5BAbstract%5D)+AND+(%222010%22%5BPublication+Date%5D+%3A+%222017%22%5BPublication+Date%5D)

# one needs to check if author was given etc. but if yes:
url = "https://www.ncbi.nlm.nih.gov/pmc/?term="
query = url +  args.author + "[author]" 
print(query)
#it would be run as:
#python sysReview_search.py --author="Olivia Keiser"

#try:
#    os.makedirs("../../Output/")
#except OSError as e:
#    if e.errno != errno.EEXIST:
#        raise
     

#output_pdf = "../../Output/output_" + query + "_pdf"
#output_txt = "../../Output/output_" + query + "_txt"
#summary_file = "../../Output/summary_" + query + ".txt"
#keywords_file = "../../Output/kw_" + query + ".csv"

#parse(query, output_pdf)
#convert(output_pdf, output_txt, summary_file)
#txt2keyphrases(output_txt, keywords_file)
