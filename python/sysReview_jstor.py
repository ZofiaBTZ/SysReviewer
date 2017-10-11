from paperity2pdf import parse
from pdf2txt import convert
from txt2key_phrases import txt2keyphrases
import os, errno
import sys

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
keywords_file = "../../Output/kw_" + query + ".csv"

parse(query, output_pdf)
convert(output_pdf, output_txt, summary_file)
txt2keyphrases(output_txt, keywords_file)
