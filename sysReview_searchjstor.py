
from paperity2pdf import parse
from pdf2txt import convert
from txt2key_phrases import txt2keyphrases
import os, errno
import sys
import argparse
import webbrowser, datetime




parser = argparse.ArgumentParser(description= "Articles search arguments in JSTOR", add_help=True)
group = parser.add_mutually_exclusive_group()

#Define validity of search period /date
def valid_date(s):
    try:
        t= datetime.datetime.strptime(s, "%Y")
        return t.strftime("%Y")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)

#Add all necessary arguments
parser.add_argument("--startdate", "-sd",
                    help="Search start date - format",
                                     type=valid_date, dest="startdate")

parser.add_argument("--enddate", "-ed",
                    help="Search end date - format",
                                     type=valid_date, dest="enddate")

parser.add_argument('--author', '-a', required=False,default= "", help='Author',action="store", dest= "author")
parser.add_argument('--pagenumber', '-p',default= 1,type=int,help='Page number',action="store", dest= "pagenumber")
parser.add_argument('--keywords', '-k', required=True, help='Search keyword', action="store", dest="keyW")
parser.add_argument("--output", "-o",default=True, help="Output the " + \
                    "query to a file", action="store_true", dest="Output")

group.add_argument('--quiet','-q', action='store_true', help='print quiet')
group.add_argument('--verbose','-v', default=True,action='store_true', help='print verbose')

#Printing the parsed arguments
print parser.parse_args()
args = parser.parse_args()
print "Articles published from %s  to %s" % (args.startdate, args.enddate)
print "By :%s " % (args.author)
print "Keywords :%s " % args.keyW
print "Results page number :%s " % args.pagenumber
print "Query saved? =%s " % args.Output

#Checking if required and necessary arguments are parsed
if args.author or args.keyW or args.startdate or args.enddate:
    url = "https://www.jstor.org/action/doAdvancedSearch"
    query = url + "?f5=all&pt=&f4=all&c1=AND&f2=all&f0=all&q3=&group=none&c4=AND&isbn=&f3=all&q6=&sd=" + str(args.startdate) + "&c6=AND&q0=" + str(args.keyW) \
	+ "&q5=&c3=AND&la=&q1=" + args.author + "&q2=&f1=au&c5=AND&f6=all&acc=off&c2=AND&q4=&ed=" + args.enddate
else :
    print("Incomplete search. Please enter required information : Author's name and Keywords")

#Writing the queries to a text file
if  args.Output :
    f = open("query.txt","a")
    f.write(str(query) + '\n')

#Requesting for quite or verbose execution
if __name__ == "__main__":
    if args.quiet :
        print query
    elif args.verbose :
        print("verbosity turned on")
        print("URL and search query :", query)
        webbrowser.open(query)

#it would be run as:
#python sysReview_search.py --author "Olivia Keiser" --keywords "HIV in Malawi" --startdate "2000" --enddate "2017"