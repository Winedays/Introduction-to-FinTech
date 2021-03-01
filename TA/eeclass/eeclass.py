import os
import re
import sys
import csv
import argparse
from bs4 import BeautifulSoup
import requests  #使用requests套件的requests.get()方法
from datetime import datetime, timedelta
from argparse import ArgumentParser
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart

'''
How to get the date N days ago in Python : https://www.saltycrane.com/blog/2010/10/how-get-date-n-days-ago-python/
Python date string to date object : https://stackoverflow.com/questions/2803852/python-date-string-to-date-object
Python strptime() format directives : https://www.journaldev.com/23365/python-string-to-datetime-strptime
PTT 網路版爬蟲 : https://github.com/afunTW/ptt-web-crawler
Beautiful Soup 4.4.0 文档 : https://beautifulsoup.readthedocs.io/zh_CN/v4.4.0/index.html?highlight=extract
'''

def readStudentsCSV( file ) :
    studentData = []
    
    f = open( file , 'r' , encoding = 'utf-8' )
    rows = csv.reader( f )
    next(rows) # skip title
    for row in rows :
        studentData.append( [row[5] , row[4]] ) # name , id
        
    return studentData

def registerAccount( name , id ) :
    # board index page
    url = "http://eeclass.formosasoft.com/index/register"
    
    try :
        
        # get csrf_t of register
        request = requests.get( url , params={'next': '/index/'} )
        soup = BeautifulSoup(request.text, 'html.parser')
        csrf_t = soup.find( "input", type="hidden", attrs={"name": "csrf-t"} )["value"]
        # print( csrf_t )
        
        # register a account 
        student_params = {"_fmSubmit": "yes", "formVer": "3.0", "formId": "register_form", 
            "account": id, "fullName": name , 
            "password": id[-6:], "password2": id[-6:], "email": "",
            "reg_note": "fintech student", "agreeMsg": 1, "csrf-t": csrf_t}
        request = requests.get( url , params=student_params )
        print( "register success , id :" , id , "pw :" , id[-6:] )
        print( request.text )

    except Exception as e :
        print("Error fail : " , e )
    
    return ;

if __name__ == "__main__" :  
    # get students data
    StudentsData = readStudentsCSV( "./41883e.csv" )
    print( StudentsData )
    print( len(StudentsData) )
    
    for student in StudentsData :
        name = student[0]
        id = student[1]
        registerAccount(name, id) # name , id 
        # print( name , id )
        
