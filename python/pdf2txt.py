import os
import glob
import sys
import errno
import subprocess
import re
import collections
#import xlsxwriter
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


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()
    return str

#add proper parsing of arguments
# if ocr needed -- https://pythontips.com/2016/02/25/ocr-on-pdf-files-using-python/

def remove_non_ascii(text):
    text = re.sub(r'[\357\254\200]+', 'ff', text)
    text = re.sub(r'[\357\254\201]+', 'fi', text)
    text = re.sub(r'[\357\254\202]+', 'fl', text)
    text = re.sub('fffi ', 'fi', text)
    text = re.sub('ff ', 'ff', text)
    text = re.sub('[^0-9a-zA-Z]+', ' ', text)
 #   text = re.sub(r'[^\x00-\x7F]+',' ', text) 
    return(text)

def get_toc(pdf_path):    #pdf structure of the file
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

# TODO: change input, not order dependent
#   parser = argparse.ArgumentParser(description='Description of your program')
#parser.add_argument('-f','--foo', help='Description for foo argument', required=True)
#parser.add_argument('-b','--bar', help='Description for bar argument', required=True)
#args = vars(parser.parse_args()) 

###pdf_dir = sys.argv[1]
###summary_file = txt_dir + "/summary.txt" #sys.argv[3]
#last_file = '0'
###txt_dir = sys.argv[2]

def convert(pdf_dir, txt_dir, summary_file):
    summary = open(summary_file, "w")
    try:
        os.makedirs(txt_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
     
    #os.chdir(pdf_dir)
    for f in glob.glob(pdf_dir + "/" + "*.pdf"):
        print(f)
        # if f > last_file:    
        try:
            retvalue = convert_pdf_to_txt(f)
            retvalue = remove_non_ascii(retvalue)
            file_name =  os.path.basename(f)
            txt_name = file_name.replace(".pdf", ".txt")
            txt_path = txt_dir +"/"+ txt_name
            print(txt_path)
            print(os.getcwd())
            with open(txt_path, "w+") as ff:
                ff.write(retvalue)
        except:
            print(f + "   not parsed")
            continue            
        
        summary.write(f)
    
        toc = get_toc(f)
        if toc == list():
            toc = retvalue.split('.')[0]
            #print(toc)
        else:
            toc = ' '.join(get_toc(f))
            #print(toc)
        summary.write(toc)
        summary.write(" \n")
    summary.close()

    

    
# check the title --- more points for word in the title. Don't look for words in Bibliography
