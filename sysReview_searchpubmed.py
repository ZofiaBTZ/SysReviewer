from paperity2pdf import parse
from pdf2txt import convert
from txt2key_phrases import txt2keyphrases
import os, errno
import sys
import argparse
import webbrowser, datetime




parser = argparse.ArgumentParser(description= "Articles search arguments", add_help=True)
group = parser.add_mutually_exclusive_group()

#Define validity of search period /date
def valid_date(s):
    try:
        t= datetime.datetime.strptime(s, "%Y")
        return t.strftime("%Y")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


parser.add_argument("--startdate", "-sd",
                    help="Search start date - format",
                                     type=valid_date, dest="startdate")
parser.add_argument("--enddate", "-ed",
                    help="Search end date - format",
                                     type=valid_date, dest="enddate")

parser.add_argument('--author', '-a', required=True,help='Author',action="store", dest= "author")
parser.add_argument('--keywords', '-k', required=True, help='Search keyword', action="store", dest="keyW")
parser.add_argument('--databases', '-db',required=True,help='Article databases',action="store", dest="dataBases", \
						choices= ["pmc","pubmed"])
parser.add_argument("--output", "-o", help="Output the " + \
					"query to a file",default= True, action="store_true", dest="Output")

group.add_argument('--quiet','-q', action='store_true', help='print quiet')
group.add_argument('--verbose','-v', default=True,action='store_true', help='print verbose')

print parser.parse_args()
args = parser.parse_args()
print "Articles published from %s  to %s" % (args.startdate, args.enddate)
print "By :%s " % (args.author)
print "Keywords :%s " % args.keyW
print "Query saved? =%s " % args.Output

#Checking for required arguments 
#Basic url and query
if args.author or args.keyW or args.dataBases or args.startdate or args.enddate:
	url = "https://www.ncbi.nlm.nih.gov/" + str(args.dataBases) + "/?term="
	query = url +  args.author + "[author]" + "+AND+" + args.keyW + "+AND+" + str(args.startdate) + "[Publication Date]" + "+%3A+" + str(args.enddate) + "[Publication Date]"
	
else :
	print("Incomplete search. Please enter required information : Author's Fullname, Keywords, database, start date and end date")

if  args.Output :
	f = open("query.txt","a")
	f.write(str(query) + '\n')

if __name__ == "__main__":
	if args.quiet :
		print query
	elif args.verbose :
		print("verbosity turned on")
        print("URL and search query :", query)
    	webbrowser.open(query)


#it would be run as:
#python sysReview_search.py --author="Olivia Keiser" --keywords "HIV in Malawi" --database "pubmed" --startdate "2000" --enddate "2017"

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
