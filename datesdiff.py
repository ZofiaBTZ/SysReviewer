import datetime
import calendar
import os
#This module should provide startdate and enddate

#os.system('python sysReview_searchjstor.py --keywords' + str(keywords) + '--startdate' + str(startdate)+ '--enddate'+ str(enddate) )
# subprocess.call(["python", "sysReview_searchjstor.py --keywords' + str(keywords) + '--startdate' + str(startdate)+ '--enddate'+ str(enddate) "])
# from sysReview_searchjstor import *  # To Do : Running sysReview_searchjstor in jstor_search (Command line??)
#                                   #Shell commands to pass on required arguments i.e. keywords, startdate and enddate

#from sysReview_searchjstor import args.startdate, args.enddate
# date1 = args.startdate
#date2 = args.enddate
# date1 = raw_input ("Enter start date : ")
# date2 = raw_input("Enter end date : ")

def difference(start, end):
    years = end.year - start.year
    months = end.month - start.month
    days = end.day - start.day
    hours = end.hour - start.hour
    minutes = end.minute - start.minute
    seconds = end.second - start.second
    if seconds < 0:
        minutes -= 1
        seconds += 60
    if minutes < 0:
        hours -= 1
        minutes += 60
    if hours < 0:
        days -= 1
        hours += 24
    if days < 0:
        months -= 1
        days += calendar.monthrange(start.year, start.month)[1]
    if months < 0:
        years -= 1
        months += 12
    return { 
           'years' : years
        # 'months': months, 
        # 'days': days,
        # 'hours': hours,
        # 'minutes': minutes,
        # 'seconds': seconds
    }


startdate = datetime.datetime.strptime((date1), "%Y")
enddate = datetime.datetime.strptime((date2),"%Y")

dif = enddate.year - startdate.year
diff = difference(startdate, enddate)
print dif
print(diff)
