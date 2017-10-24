from paperity2pdf import parse
from pdf2txt import convert
from txt2key_phrases import txt2keyphrases
import os, errno
import sys
import argparse
import webbrowser, datetime




parser = argparse.ArgumentParser(description= "Parsing articles search arguments", add_help=True)
group = parser.add_mutually_exclusive_group()

def valid_date(s):
    try:
        t= datetime.datetime.strptime(s, "%Y-%m-%d")
        return t.strftime("%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)

#parser.add_argument('--date', '-d', help='Date of publication',action="store_true", dest = "pubDate")
parser.add_argument("--date", "-d",
                    help="Date of publication- format YYYY-MM-DD", 
                                     type=valid_date, dest="date")
#parser.add_argument('--year', '-y', help='Year of publication -format YYYY-MM-DD',action="store_true", dest = "year")
parser.add_argument('--author', '-a', required=True,help='Author',action="store", dest= "author")
parser.add_argument('--keywords', '-k', required=True, help='Search keyword', action="store", dest="keyW")
parser.add_argument('--databases', '-db',required=True,help='Article databases',action="store", dest="dataBases", \
						choices= ["pmc","pubmed"])
parser.add_argument("--output", "-o", help="Output the " + \
					"query to a file", action="store_true", dest="Output")

group.add_argument('--quiet','-q', action='store_true', help='print quiet')
group.add_argument('--verbose','-v', action='store_true', help='print verbose')

print parser.parse_args()
args = parser.parse_args()
#print args.pubDate
print args.date
print args.author
print args.keyW
print args.dataBases
print args.Output


#https://www.ncbi.nlm.nih.gov/pmc/?term=(((Keiser,+Olivia%5BAuthor%5D)+AND+HIV%5BAbstract%5D)+AND+Malawi%5BAbstract%5D)+AND+(%222010%22%5BPublication+Date%5D+%3A+%222017%22%5BPublication+Date%5D)
#https://www.ncbi.nlm.nih.gov/pubmed/?term=%3DOlivia+Keiser%5Bauthor%5D+HIV+in+Malawi


if args.author or args.keyW or args.pubDate or args.dataBases or args.date:

# one needs to check if author was given etc. but if yes:
	url = "https://www.ncbi.nlm.nih.gov/" + str(args.dataBases) + "/?term="
	query = url +  args.author + "[author]" + args.keyW + str(args.date)
	#print("Search query is :",query)
	#webbrowser.open(query)

else :
	print("Incomplete search. Please enter required information : Author Fullname, Keyword,Date and Database")

if  args.Output :
	f = open("query.txt","a")
	f.write(str(query) + '\n')

if __name__ == "__main__":
	if args.quiet :
		print query
	elif args.verbose :
		print("Search query is :",query)
		webbrowser.open(query)


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
