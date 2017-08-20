A tool to download and process the articles from the articles database (at the moment www.paperity.com, soon https://www.ncbi.nlm.nih.gov/pubmed/ and others).
SysReviewer downloads available .pdf from the search results.
The .pdfs are processed to .txt.
RAKE algorithm is used for .txt file to find most frequent phrases. The table of phrases and their freqencies for papers is returned.
All outputs are saved in a directory:
../Output.
The .pdf files are saved in:
../Output/Output_<searched_phrase>_pdf
The .txt files are saved in:
../Output/Output_<searched_phrase>_txt
The key phrases are saved as:
../Output/kw_<searched_phrase>.csv

Getting started:
Download the SysReviewer repository from the github. Extract in your home folder. In the directory ./python run an example from the'Usage' section.

Requirements:
Python 2.7, nltk, csv, pdfminer, bs4, requests, urllib2

Usage:
> python sysReview.py kwashiorkor


will download papers, which has kwashiorkor in any field. The output will be saved in:
The .pdf files are saved in:
../Output/Output_kwashiorkor_pdf
The .txt files are saved in:
../Output/Output_kwashiorkor_txt
The key phrases are saved as:
../Output/kw_kwashiorkor.csv


> python SysReview.py "Malawi AND HIV AND DHS"



will download the papers which have Malawi, HIV and DHS in any of the fields.
The .pdf files are saved in:
../Output/Output_Malawi+AND+HIV+AND+DHS_pdf
The .txt files are saved in:
../Output/Output_Malawi+AND+HIV+AND+DHS_txt
The key phrases are saved as:
../Output/kw_Malawi+AND+HIV+AND+DHS.csv


At the moment, only search for any of field is available. 
Soon there will be added year, author, keywords and other databases of papers.
TODO:
-more databases of articles
-search options as powerful as in data base
-report on downloaded and parsed papers
-cleaner keypharases
-parameterisation of the keyphrases algorithm


Thanks for useful manuals to:
to add

