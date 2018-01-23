import os
import glob
import sys
import errno
import subprocess
import re
import collections
import sys
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument, PDFNoOutlines
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure, LTImage
from pdfminer.converter import TextConverter
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

reload(sys)
sys.setdefaultencoding('utf8')

#Converts the PDF file to a TXT file
def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()                                                  #Creates a PDF resource manager objects that stores shared resources.
    retstr = StringIO()                                                             #Creates an object that reads and writes a string buffer
    codec = 'utf-8'
    laparams = LAParams()                                                           #Set parameters for the text analysis
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)         #Converts the text
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)                               #Process the page content
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):   #For all pages, extracts the text
        interpreter.process_page(page)
    fp.close()
    device.close()
    str = retstr.getvalue()                                                         #Resets retstr otherwise gets copies
    retstr.close()
    return str                                                                      #Returns the text


#Removes non ASCII characters
def remove_non_ascii(text):
    text = re.sub(r'[\357\254\200]+', 'ff', text)
    text = re.sub(r'[\357\254\201]+', 'fi', text)
    text = re.sub(r'[\357\254\202]+', 'fl', text)
    text = re.sub('fffi ', 'fi', text)
    text = re.sub('ff ', 'ff', text)
    text = re.sub('[^0-9a-zA-Z]+', ' ', text)
    text = re.sub(r'[^\x00-\x7F]+',' ', text) 
    return(text)

#Extracts the table of content from the pdf
def get_toc(pdf_path):    
    infile = open(pdf_path, 'rb')
    parser = PDFParser(infile)
    document = PDFDocument(parser)
    toc = list()
    try:
        for (level,title,dest,a,structelem) in document.get_outlines():
            print remove_non_ascii(title.strip()) 
            toc = '-'
    except PDFNoOutlines:
        pass
    return toc


def convert(pdf_dir, txt_dir, summary_file):
    summary = open(summary_file, "w")
    try:                                                                #Checks if the directory for txt outputs exists, otherwise creates it
        os.makedirs(txt_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    for f in glob.glob(pdf_dir + "/" + "*.pdf"):                        #Loops over all the PDF files located in the PDF folder
        print(f)

        #Creates a TXT file with the same name as the PDF file
        file_name = os.path.basename(f)
        txt_name = file_name.replace(".pdf", ".txt")
        txt_path = txt_dir +"/"+ txt_name
        #Converts to TXT
        if (os.path.isfile(txt_path)):                                  #Checks if the txt file already exists, if yes, then the conversion was alredy made
            print ("Already converted")
        else:      
            try:                                                            
                retvalue = convert_pdf_to_txt(f)                            #Converts the PDF file to txt
                #print(retvalue[1:6])
                retvalue = remove_non_ascii(retvalue)                       #Removes the non ASCII characters
                #file_name =  os.path.basename(f)
                #txt_name = file_name.replace(".pdf", ".txt")                #Creates a TXT file with the same name as the PDF file
                #txt_path = txt_dir +"/"+ txt_name
                #print(txt_path)
                #print(os.getcwd())
                with open(txt_path, "w+") as ff:                            #Writes the extracted text in the TXT file
                    ff.write(retvalue)
            except:
                print(f + "   not parsed")                                  #add to summary
                continue            
            summary.write(f)
            toc = get_toc(f)                                                #Process the table of content of the PDF file
            if toc == list():                                               #If empty
                toc = retvalue.split('.')[0]
            else:                                                           #Else get the toc
                toc = ' '.join(get_toc(f))
            summary.write(toc)
            summary.write(" \n")
    summary.close()

    

    
# check the title --- more points for word in the title. Don't look for words in Bibliography
## titles from numbers to real titles
