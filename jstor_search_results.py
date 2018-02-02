# import libraries
import urllib2,cookielib
import requests
import re
import sys
from bs4 import BeautifulSoup
import subprocess
import os
#os.system('python datesdiff.py')     #Relies on sysReview_searchjstor
#from datesdiff import dif

# #User Input
# keywords = raw_input ("Please enter the keywords : ")
# startdate = raw_input ("Please enter start date : ")
# enddate = raw_input ("Please enter end date : ")

# import os
# os.system('python sysReview_searchjstor.py --keywords' + str(keywords) + '--startdate' + str(startdate)+ '--enddate'+ str(enddate) )
# subprocess.call(["python", "sysReview_searchjstor.py --keywords' + str(keywords) + '--startdate' + str(startdate)+ '--enddate'+ str(enddate) "])
# from sysReview_searchjstor import *  # To Do : Running sysReview_searchjstor in jstor_search (Command line??)
# 									#Shell commands to pass on required arguments i.e. keywords, startdate and enddate

# specify the url
#query has to come from  sysReview_searchjstor module
#User has to pass the arguments first..ie.keywords, startdate and enddate

#quote_page = query   #after running sysReview_searchjstor
quote_page = 'https://www.jstor.org/action/doAdvancedSearch?f5=all&pt=&f4=all&c1=AND&f2=all&f0=all&q3=&group=none&c4=AND&isbn=&f3=all&q6=&sd=2000&c6=AND&q0=HIV%20in%20Malawi&q5=&c3=AND&la=&q1=&q2=&f1=au&c5=AND&f6=all&acc=off&c2=AND&q4=&ed=2017'


hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

req = urllib2.Request(quote_page,headers=hdr)
contents = urllib2.urlopen(req).read()
#print contents

try:
    page = urllib2.urlopen(req)
except urllib2.HTTPError, e:
    print e.fp.read()

# parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(contents, "lxml")

#cleaning out the tags and unnecessary characters
#Search results
temp = soup.find('h1').get_text()
temp1= soup.find('li', id = "startDate").get_text()
temp2= soup.find('li', id = "endDate").get_text()

#Keep numeric only
search_results = re.sub('[^0-9]', '', temp)
startdate = re.sub('[^0-9]', '', temp1)
enddate = re.sub('[^0-9]', '', temp2)

#Print the outputs
print search_results
print startdate
print enddate

#Set maximum number of papers
max_papers = 1000
print "Your initial search period is from %s to %s" % (startdate, enddate)   
#print "Your initial search period is from %s to %s" % (args.startdate, args.enddate)   #(from sysReview_searchjstor)

#new_enddate = 0
#Stratification by search period starts from here

#Search period range
# avgdiff = (dif /2 )
# print dif
# print avgdiff

#while search_results >= max_papaers:
if search_results >= max_papers:
	startdate = startdate         #startdate = args.startdate
	enddate = int(startdate) + 2  #enddate = startdate + avgdiff
	print "New search period is now from %s to %s" % (startdate, enddate)
	#Another half of search period
	#startdate = enddate + 1
	#enddate = args.enddate
else :
	#search (startdate,enddate,keywords)
	print "Within the range"
	#os.system('python sysReview_searchjstor.py')
