import urllib2
from bs4 import BeautifulSoup
import requests
from urllib2 import Request, urlopen
from pyPdf import PdfFileWriter, PdfFileReader
from StringIO import StringIO
import datetime
import os
import errno

# create list of dois to add entries into Zotero
# e. prepare bibtex file
def download_file(url, output):
    f = open(output, 'wb')
    webFile = urllib2.urlopen(url)
    f.write(webFile.read())
    webFile.close()
    f.close()

def download_header_file(url, fname):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url, headers = headers)
    f =open(fname, 'w')
    f.write(response.content)


def process_page(my_url, output_dir):
    pap = "https://www.jstor.org"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    r = requests.get(my_url, headers = headers)
    soup_all = BeautifulSoup(r.content, "html.parser")
    titles = soup_all.find_all("h4", {"class": "paper-list-title"})
    print("titles")
    for title in titles:
        new_t = title.find("a").get("href")
        print(new_t)
        url_paper = pap + new_t 
        html_paper = urllib2.urlopen(url_paper).read()
        print("next paper")
        print(url_paper)
        soup = BeautifulSoup(html_paper, 'html.parser')
        pdf_url = soup.find("meta", {"name":"citation_pdf_url"})['content']
        #title = soup.find("meta", {"name":"citation_title"})['content']
        file_name = new_t.split('/')[-1]
        output = output_dir + "/" + '_'.join(file_name.split()) + '.pdf'
        download_file(pdf_url, output)

       

def parse(query, pdf_dir):
    pap = "https://www.jstor.org"    
    url = "https://www.jstor.org/action/doBasicSearch?Query="
    #"http://paperity.org/search/?q="
    #url_n = "http://paperity.org/search/"
    url_n = "https://www.jstor.org/action/doBasicSearch?page="
    #2
    url_q ="&Query="
    
    #url_end = "?q="
    #today = datetime.date.today()
    q = url + query
    html = urllib2.urlopen(q).read()
    print(q)
    
    try:
        os.makedirs(pdf_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
        
    process_page(q, pdf_dir)
    i = 1
    while i<51:
        i = i + 1
        q_next = url_n + str(i) + url_end + query
        print(q_next)
        try:
            process_page(q_next, pdf_dir)
        except Exception:
            exit


download_header_file("http://www.jstor.org/stable/pdf/3583410.pdf?refreqid=excelsior%3A1927a441c3b2568c7434cb2660ff150a", "./test_jstor.pdf") 
    

