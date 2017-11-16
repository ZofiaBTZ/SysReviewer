#from paperity2pdf import parse
#from pdf2txt import convert
#from txt2key_phrases import txt2keyphrases
import os, errno
import sys
import argparse
import webbrowser, datetime


#Define validity of search period /date
def valid_date(s):
    try:
        t= datetime.datetime.strptime(s, "%Y")
        return t.strftime("%Y")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)

#Add all necessary arguments

def args2query():
    parser = argparse.ArgumentParser(description= "Articles search arguments", add_help=True)
    group = parser.add_mutually_exclusive_group()

    parser.add_argument("--startdate", "-sd",
                        help="Search start date - format",
                        type=valid_date, dest="startdate")

    parser.add_argument("--enddate", "-ed",
                        help="Search end date - format",
                        type=valid_date, dest="enddate")

    parser.add_argument('--author', '-a', required=True,default= "", help='Author',action="store", dest= "author")
    parser.add_argument('--pagenumber', '-p',default= 1,type=int,help='Page number',action="store", dest= "pagenumber")
    parser.add_argument('--keywords', '-k', required=True, help='Search keyword', action="store", dest="keyW")
    #parser.add_argument('--journal', '-j',help='Journal name', action="store", dest= "journal", \
        #choices= ["PLOS ONE","PLOS Medicine","BMC Public Health","BMC Infectious Diseases","BMC Medicine", "SpringerPlus"])
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

    #Checking if requred and necessary arguments are parsed
    if args.author or args.keyW or args.startdate or args.enddate:
        url = "http://paperity.org/search/" + str(args.pagenumber) #+ "?as_c="
        #query = url +args.keyW + "&as_au=" + args.author \
        #        + "&f_date_start=" + str(args.startdate) + "&f_date_end=" + str(args.enddate)
        query = "?as_c="  + "+".join(args.keyW.split()) + "&as_au=" + args.author \
                + "&f_date_start=" + str(args.startdate) + "&f_date_end=" + str(args.enddate)
       
        output_name = "_".join(args.keyW.split()) + "_" + args.author + "_" + str(args.startdate) + "_" + str(args.enddate) 

    else :
        print("Incomplete search. Please enter required information : Author's name and Keywords")
        query = ""
        output_name = ""
        
    #Writing the queries to a text file
    #TODO:  do it outside this function, in the folder of this search 
    #if  args.Output :
    #    f = open("query.txt","a")
    #    f.write(str(query) + '\n')
    return{'query': query, 'output_name': output_name} 

    
#Requesting for quite or verbose execution
if __name__ == "__main__":
    if args.quiet :
        print query
    elif args.verbose :
        print("verbosity turned on")
        print("URL and search query :", query)
        webbrowser.open(query)

#it would be run as:
#python sysReview_search.py --author "Olivia Keiser" --keywords "HIV in Malawi" --startdate "2000" --enddate "2016"
