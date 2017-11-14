from paperity2pdf import parse
from pdf2txt import convert
from txt2key_phrases import txt2keyphrases
from txt2keywords_tfidf import txt2tfidf
from txt2textRank import txt2textRank
import os, errno
import sys
#import contentloader

query = sys.argv[1]
query = "+".join(query.split())
print(query)


try:
    os.makedirs("../../Output/")
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
     

output_pdf = "../../Output/output_" + query + "_pdf"
output_txt = "../../Output/output_" + query + "_txt"
summary_file = "../../Output/summary_" + query + ".txt"
keyphrases_file = "../../Output/kp_" + query + ".csv"
keywords_file = "../../Output/short_kw_" + query + ".csv"
textRank_file ="../../Output/textRank_" + query + ".csv"
parse(query, output_pdf)
convert(output_pdf, output_txt, summary_file)
txt2keyphrases(output_txt, keyphrases_file)
txt2tfidf(output_txt, keywords_file)
#txt2textRank(output_txt, textRank_file)
