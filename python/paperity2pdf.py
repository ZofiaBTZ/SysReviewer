import urllib2
from bs4 import BeautifulSoup
import requests
from urllib2 import Request, urlopen
from pyPdf import PdfFileWriter, PdfFileReader
from StringIO import StringIO
import datetime
import os
import errno
from words_cooccurence_paperity import pap2freq
#from pubmed_download import parse_pubmed

# create list of dois to add entries into Zotero
# e. prepare bibtex file
def download_file(url, output, title, output_dir):                              #Downloads the pdf file linked by paperity
    f = open(output, 'wb')
    webFile = urllib2.urlopen(url)
    f.write(webFile.read())
    webFile.close()
    f.close()
##  #Checks if the file is empty (if yes, it means the pdf was not given in paperity but rather an html or possibly a corrupted file)
##  #Haven't yet checked if it works!
##    if (os.stat(output).st_size) < 30000:
##        print ("File corrupted or not available on Paperity. Checking PUBMED...")
##        os.remove(output)                                                     #Is empty, so we remove it    
##        title_pubmed = string.replace(title, "-", " ")                        #Removes the dash in title variable, otherwise PUBMED does not recognise it
##        parse_pubmed(title_pubmed, output_dir)                                #Calls the pubmed equivalent
    return


def process_page(my_url, output_dir):
    pap = "http://paperity.org"    
    r = requests.get(my_url)                                                    #access the requested URL
    soup_all = BeautifulSoup(r.content, "html.parser")                          #Gets the HTML code
    titles = soup_all.find_all("h4", {"class": "paper-list-title"})             #Looks for a h4 tag with class "paper-list-title"
    print("titles")
    for title in titles:
        new_t = title.find("a").get("href")                                     #In the title of the paper, gets the according URL to the page with the pdf link
        url_paper = pap + new_t 
        html_paper = urllib2.urlopen(url_paper).read()                          #Access the url_paper URL
        print("next paper")
        print(url_paper)
        soup = BeautifulSoup(html_paper, 'html.parser')                         #Gets the HTML code
        pdf_url = soup.find("meta", {"name":"citation_pdf_url"})['content']     #Finds the URL of the actual PDF
        file_name = new_t.split('/')[-1]
        output = output_dir + "/" + '_'.join(file_name.split()) + '.pdf'        #Creates the outputfilename
        if (os.path.isfile(output) and  os.stat(output).st_size > 30000):       #Checks if the file exists. If it does then do nothing, else download
            print("Already downloaded")                                         
        else:
            download_file(pdf_url, output, title, output_dir)
    return


#This is used to create a valid search URL
def parse(query, pdf_dir, last_page):
    #Checks how much papers there are from the woords_cooccurence_paperity python file, and makes the accurate number of pages out of it
    pap = "http://paperity.org/search/" + query
    subset = float(pap2freq(pap))
    nb_pages = int(subset/20.)+1                                                #Paperity shows 20 results per page
      
    url_n = "http://paperity.org/search/"
    
    try:                                                                        #Checks if the directory pdf_dir exists, if it doesn't create it                        
        os.makedirs(pdf_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    
    i = last_page - 1  
    while i <= nb_pages:                                                        #That should loop properly
        i = i + 1
        q_next = url_n + str(i) +  query                                        #Stores in q_next the URL of the page number of the search term.
        print(q_next)   
        try:                                                                    #Tries to see if ther is a next page, if not, exits.
            process_page(q_next, pdf_dir)
        except Exception:
            exit
    return


    

