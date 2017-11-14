from selenium import webdriver
import urllib2
from bs4 import BeautifulSoup
import requests
from urllib2 import Request, urlopen
from pyPdf import PdfFileWriter, PdfFileReader
from StringIO import StringIO
import datetime
import os
import errno
import time

def cache2html(url):
    url_hash = str(hash(url))
    try:
        f = file('../tmp/cache/a'+ url_hash)
        return f.read()
    except:
        print("downoading file")
        #print ("File not found, run the script in 2 days to have the access")
        #return ("empty ")
        
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url, headers = headers)
    f = file('../tmp/cache/a'+ url_hash, 'w')
    f.write(response.content)
    return response.content


def download_header_file(url, fname):
    #TODO  if fname does not exist in the directory!!
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url, headers = headers)
    f =open(fname, 'w')
    f.write(response.content)


def setFirefox(out_dir):
    out_dir = "./test_folder"
    fp = webdriver.FirefoxProfile()
    fp.set_preference("browser.download.folderList", 2)
    fp.set_preference("browser.download.manager.showWhenStarting",False)
    fp.set_preference("browser.download.dir", out_dir)
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf,application/x-pdf")
    fp.set_preference("pdfjs.disabled", "true")  # < KEY PART HERE
    driver =webdriver.Firefox(executable_path=r'/home/b/zbaran/Documents/Genf/sysRevieweGH/SysReviewer/python/geckodriver', firefox_profile=fp)
    print(driver)
    return driver

def setChrome(out_dir):
    fp = webdriver.Chrome(executable_path=r'/home/b/zbaran/Documents/Genf/sysRevieweGH/SysReviewer/python/chromedriver')
    fp.set_preference("browser.download.folderList", 2)
    fp.set_preference("browser.download.manager.showWhenStarting",False)
    fp.set_preference("browser.download.dir", out_dir)
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf,application/x-pdf")
    fp.set_preference("pdfjs.disabled", "true")  # < KEY PART HERE
    
    print(fp)
    return fp


def process_page_jstor(my_url, driver):
    print my_url
    jstor = "http://www.jstor.org"
    html = cache2html(my_url)
    soup_all = BeautifulSoup(html, "html.parser")
    titles = soup_all.find_all("a", {"class": " pdfLink button button-jstor"})
    print("titles")
    print(len(titles))
    print(titles)
    for title in titles:
        new_t = title.get("href")
        print(new_t)
        url_paper = jstor + new_t
        print url_paper        
        #driver.get(url_paper)
        driver = setFirefox("./")
        driver.get(url_paper)
        link = driver.find_element_by_xpath("//input[@value='I accept, proceed to PDF']")
        print(link)
        link.click()
        time.sleep(10)
        #download_header_file(url_paper, url_paper.split('/')[-1] )
        driver.quit()
        
        # to change the fle name



def parse(query, pdf_dir):
    url_start = "https://www.jstor.org/action/doBasicSearch?searchType=facetSearch&page="
    url_end = "&sd=2010&ed=2015&Query=(Malawi)"
    driver = setFirefox(pdf_dir)
    #driver.get("http://www.jstor.org/stable/pdf/4147628.pdf")
    #link = driver.find_element_by_xpath("//input[@value='I accept, proceed to PDF']")
    #print(link)
    #link.click()
        
    #pap = "https://www.jstor.org"    
    #url = "https://www.jstor.org/action/doBasicSearch?Query="
    #"http://paperity.org/search/?q="
    #url_n = "http://paperity.org/search/"
    #url_n = "https://www.jstor.org/action/doBasicSearch?page="
    #2
    #url_q ="&Query="
    
    #url_end = "?q="
    #today = datetime.date.today()
    #q = url + query
    ### NO RUN BEFORE CACHE!!!
    #headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    #response = requests.get(url, headers = headers)

    #    html = urllib2.urlopen(q).read()
    #print(q)
    #html = cache2html(q)
    #try:
    #    os.makedirs(pdf_dir)
    #except OSError as e:
    #    if e.errno != errno.EEXIST:
    #        raise

    ### continue here!!    
    #process_page(q, pdf_dir)
    i = 15
    while i<20:
        q_next = url_start + str(i) + url_end #+ query
        print(q_next)
        #try:
        process_page_jstor(q_next, driver)
        #except Exception:
        #    print("cannot process the url ")
        #    exit
        i = i + 1


#driver.get("http://www.jstor.org/stable/pdf/4147628.pdf")



#download_header_file("http://www.jstor.org/stable/pdf/3583410.pdf", "./test_jstor.pdf") 


parse("", "../output_jstor/")
