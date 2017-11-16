from paperity2pdf import parse
from pdf2txt import convert
from txt2key_phrases import txt2keyphrases
from txt2keywords_tfidf import txt2tfidf
from txt2textRank import txt2textRank
from sysReview_searchpaperity import args2query
import os, errno
import sys
#import contentloader

#query = sys.argv[1]
#query = "+".join(query.split())
parsed = args2query()
query = parsed["query"]
output_name = parsed["output_name"]
print(query)
print(output_name)

try:
    os.makedirs("../../Output/")
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
     

output_pdf = "../../Output/output_" + output_name + "_pdf"
output_txt = "../../Output/output_" + output_name + "_txt"
summary_file = "../../Output/summary_" + output_name + ".txt"
keyphrases_file = "../../Output/kp_" + output_name + ".csv"
keywords_file = "../../Output/short_kw_" + output_name + ".csv"
textRank_file ="../../Output/textRank_" + output_name + ".csv"
parse(query, output_pdf)
convert(output_pdf, output_txt, summary_file)
txt2keyphrases(output_txt, keyphrases_file)
txt2tfidf(output_txt, keywords_file)
#txt2textRank(output_txt, textRank_file)
