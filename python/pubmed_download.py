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


def process_html_pubmed(html,pdf_dir):
    pubmed_basic = "https://www.ncbi.nlm.nih.gov/"
    pubmed_link = "www.ncbi.nlm.nih.gov/" 
    plos_link = "www.journals.plos.org/plosone/article/file?id="
    elsevier_link = "www.linkinghub.elsevier.com/"
    ovid_link ="www.Insights.ovid.com/"
    sage_link = "www.journals.sagepub.com/"
    springer_link = "https://dx.doi.org/10.1007/s"
    biomed_link = "https://globalizationandhealth.biomedcentral.com"
    bmj_link = "http://sti.bmj.com/"
    nejm_link = "http://www.nejm.org/"
    tandfonline_link = "http://www.tandfonline.com"
    libert_link = "http://dx.doi.org/10.1089/aid"
    jia_link = "www.jiasociety.org"
    soup_all = BeautifulSoup(html, "html.parser")
    titles = soup_all.find_all("a", href=True, ref=True)
    for title in titles:
        if ("linksrc=docsum_title" in title.get('ref')): 
            link = title.get('href')
            print(link)
            url_paper = pubmed_basic + link #pap + new_t
            html_paper  = cache2html(url_paper)
            soup = BeautifulSoup(html_paper, 'html.parser')
            titles = soup_all.find_all("a", href=True, free_status='free')
            if len(titles) == 0:
                #print("dois, 0,  ", my_url )
                titles = soup_all.find_all("a", href=True, journal=True)
                #print titles
            if len(titles) == 0:
                titles = soup_all.find_all("a", href = True, title = "Full text at publisher\'s site")
                # print titles

            for title in titles:
                link = title.get('href')
                if pubmed_link in link:
                    pdf_url = soup.find("link", href= True,  type='application/pdf')
                    name = soup.find("title").string
                    db_link = "http://" + pubmed_link
            
                if plos_link in link:
                    pdf_url = soup.find("a", href= True,  id='downloadPdf')
                    name = soup.find("title").string
                    db_link = plos_link
            
                if elsevier_link in link:
                    pdf_url = soup.find("a", href= True, class_='pdf-download-btn-link')
                    name = soup.find("title").string
                    db_link = "sciencedirect.com"

                if ovid_link in link:
                    pdf_url = soup.find("a", href= True, class_='btn-bottom-viewonjournalsite wk-button btn-fixed')
                    name = soup.find("title").string
                    db_link = ""

                if sage_link in link:
                    td = soup.find("td", class_="pdfBadge")
                    pdf_url = td.find("a", href= True)
                    name = soup.find("meta", name="dc.Title").get('content')
                    db_link =sage_link
        
                if springer_link in link:
                    pdf_url = soup.find("meta", name="citation_pdf_url").get('content')
                    name =soup.find("meta", name="citation_title").get("content") 
                    db_link = ""

                if biomed_link in link:
                    pdf_url = soup.find("meta", name="citation_pdf_url").get('content')
                    name =soup.find("meta", name="dc.title").get("content") 
                    db_link = ""

                if bmj_link in link:
                    pdf_url = soup.find("meta", name="citation_pdf_url").get('content')
                    name =soup.find("meta", name="citation_title").get("content") 
                    db_link = ""

                if nejm_link in link:
                    pdf_url = soup.find("a", href=True, class_="zone-tools-articlePdf") 
                    name =soup.find("meta", name="dc.Title").get("content") 
                    db_link = nejm_link
            
                if tandfonline_link in link:
                    pdf_url =  soup.find("a", href=True, class_="show-pdf") 
                    name =soup.find_all("meta", name="dc.Title")
                    name = name[0].get("content")
                    db_link = tandfonline_link

                if libert_link in link:
                    li = soup.find("li", class_ = "pdfprint" )
                    pdf_url = li.find("a", href = True)
                    name = soup.find("title").string 
                    db_link = "http://online.liebertpub.com/"

            #if jia_link in link:
            #    name = soup.find("title").string
            #    pdf_url = 
        
            print("pdf_url:")
            print(pdf_url)
            if not pdf_url:
                print("Link to process:")
                print(link)
        
            if pdf_url:
                final_url =  db_link + pdf_url.get('href')
                print("shoud be downloaded:")
                print(final_url)
            
                output = output_path + "/" + '_'.join(remove_non_ascii(name).split()) + '.pdf'
                download_file(final_url, output)
                return(1) # processing one paper, if downloaded no need to check 
        
            


        
def parse_pubmed(query, pdf_dir):
    url_start = "https://www.ncbi.nlm.nih.gov/pubmed/?term="
    #"https://www.jstor.org/action/doBasicSearch?searchType=facetSearch&page="
    #url_end = "&sd=2010&ed=2015&Query=(Malawi)"
    url = url_start + query
    #process_page_pubmed(url)
    driver = setFirefox(pdf_dir)
    page = 0
    while page < 2: #or till the last paper
        #next_page = selenium click page 
        driver.get(url)
        r = cache2html(url)
        soup_all = BeautifulSoup(r, "html.parser")
        titles = soup_all.find_all("a", href=True, ref=True)
        print("start_titles###########################")
        #print(titles)
        print("end titles ######################")
        link = driver.find_element_by_xpath("//a[@title = 'Next page of results']")
        #link = driver.find_element_by_xpath("//input[@value='I accept, proceed to PDF']")
        print(link)
        url_new = link.click()
        driver.implicitly_wait(10)
        print("new url ------------------------")
        print(driver.page_source)
        print("end new url---------------------")
        #q_next = url_start + str(i) + url_end #+ query
        #print(q_next)
        #try:
        #process_page_jstor(q_next, driver)
        #except Exception:
        #    print("cannot process the url ")
        #    exit
        page = page + 1


#driver.get("http://www.jstor.org/stable/pdf/4147628.pdf")



#download_header_file("http://www.jstor.org/stable/pdf/3583410.pdf", "./test_jstor.pdf") 


#parse("", "../output_jstor/")

parse_pubmed("Malawi", "../output_pubmed/")
