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



def download_header_file(url, fname):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url, headers = headers)
    f =open(fname, 'w')
    f.write(response.content)




fp = webdriver.FirefoxProfile()
fp.set_preference("browser.download.folderList", 2)
fp.set_preference("browser.download.manager.showWhenStarting",False)
fp.set_preference("browser.download.dir", "./")
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf,application/x-pdf")
fp.set_preference("pdfjs.disabled", "true")  # < KEY PART HERE

driver = webdriver.Firefox(executable_path=r'/home/b/zbaran/Documents/geckodriver', firefox_profile=fp)
driver.get("http://www.jstor.org/stable/pdf/4147628.pdf")

link = driver.find_element_by_xpath("//input[@value='I accept, proceed to PDF']")
print(link)
link.click()


download_header_file("http://www.jstor.org/stable/pdf/3583410.pdf", "./test_jstor.pdf") 
