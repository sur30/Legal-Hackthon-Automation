from bs4 import BeautifulSoup as Soup
from time import time
import requests
import json
import re
import os
#import excelHelper
from selenium import webdriver 
from selenium.common.exceptions import NoSuchElementException 
from selenium.webdriver.common.keys import Keys
#import excelHelper
#import dbHandler
import time
#import CreateCSV
import multiprocessing 
from multiprocessing import Pool
import random
import urllib
import csv
import traceback
#import dbHandler as db 
import glob
import selenium.webdriver.support.ui as ui
import re
#import support as s

#profile = webdriver.FirefoxProfile()

browser = webdriver.Firefox()
def open_browser():
    
    base_url='http://uscode.house.gov/'
    browser.get(base_url)
    
    #keywords_list = [['4','@Eagles'],['2','@Giants'],['11','@Redskins'],['31','@dallascowboys']]
    rowcounter=1
    try:
        co=1
        with open('test_new.csv', 'wb') as fp:
            a = csv.writer(fp, delimiter=',')
            while rowcounter <2:
                info = []

                #time.sleep(5)
               
                #search = "https://twitter.com/search?f=realtime&q="+team+"%20since%3A"+start_date+"%20until%3A"+end_date+"&src=typd"
                #search = "https://twitter.com/search?f=realtime&q=%23PhiladelphiaEagles%20OR%20%23Eagles%20%40Eagles%20since%3A2013-09-01%20until%3A2013-09-02&src=typd"
                if rowcounter ==0:
                    search = "http://uscode.house.gov/"
                    browser.get(search)
                else:
                    search = raw_input("Please enter the url ")
                    #search = "http://uscode.house.gov/view.xhtml?req=death+penalty&f=treesort&fq=true&num=28&hl=true&edition=prelim&granuleId=USC-prelim-title8-section1534"
                    #search = "http://uscode.house.gov/view.xhtml?req=economic+espionage&f=treesort&fq=true&num=8&hl=true&edition=prelim&granuleId=USC-prelim-title18-section1831"
                    browser.get(search)
                
                rowcounter= rowcounter+1
                #else:
                    
                    #browser.get(newsearch)
                #print "search",search
                
                #con= browser.find_element_by_class_name("stream-end")

                #con= browser.find_element_by_class_name("stream-end")
                #print con
                
               
                time.sleep(10)
                        
                #JavascriptExecutor jse = (JavascriptExecutor)browser;
                #jse.executeScript("window.scrollBy(0,250)", "");
                page = browser.page_source.encode('utf-8')
                #html_twitter =(open("first_try2"+'.html','wb+'))
                #html_twitter.write(page)
                #time.sleep(2)
                #con= browser.find_element_by_class_name("content")
                #con= browser.find_element_by_id("stream-items-id")
                #print con
                #for li in list(con.find_element_by_class_name("stream-item")):
                    #print li.get('id')

                #con = browser.find("div",{"class":"stream-item-header"})
                #cn= con.source.encode('utf-8')
                soup = Soup(page,'html.parser')
                #print soup
                #links = soup.findAll("a",href=True)
                #div = browser.find_element_by_class_name("div",{"class":"subjects_list"})
                
                div = soup.findAll("p", { "class" : "note-body" })
                div1 = soup.findAll("p", { "class" : "source-credit" })
                #div_post = soup.findAll("div", { "class" : "fonts_resizable_subject subject_title " })
                #print "len div",len(div)
                #print div
                #div = []
                div.extend(div1)
                links = div
                #print type(links)
                #print len(links)
                #links_set = set(links)
                #links = list(links_set)
                #print "links = ",links
                dup_list = []
                for di in div:
                    post = []
                    #print "di ",type(di) , di
                    #print "dup ",type(dup_list), dup_list
                    law = di.find("plaw")
                    #print law
                    #print type(law)
                    if law is not None:
                        public_law = law.text.encode('utf-8','replace')
                    else:
                        public_law= "112-296"
                    str_public_law = str(public_law)
                    if str_public_law in dup_list:
                        pass
                    else:
                        dup_list.append(str(public_law))

                        
                        #print "public law= ",law.text.encode('utf-8','replace')
                        law1 = public_law.split(" ")
                        start_first = law1[len(law1)-1]
                        #print start_first
                        #print type(start_first)
                        p1 = str(start_first)
                        #print p1
                        #print start_first.text.encode('utf-8','replace')
                        us_code_str ="" 
                        us_code = p1[0:3]
                        us_code_str = us_code
                        print "Public law",str(public_law)
                        print "congress number",us_code
                        if us_code[1:3] == '11' or us_code[1:3] == '12' or us_code[1:3] == '13' :
                            us_code_str = us_code_str +"th"
                        else:
                            if us_code[2:3] == '1':
                                us_code_str = us_code_str +"st"
                            elif us_code[2:3] == '2': 
                                us_code_str = us_code_str +"nd"
                            elif us_code[2:3] == '3':
                                us_code_str = us_code_str +"rd"
                            else:
                                us_code_str = us_code_str +"th"

                        url_congress = "https://www.congress.gov/public-laws/"+us_code_str.strip()+"-congress"
                        #print url_congress
                        browser.get(url_congress)
                        page1 = browser.page_source.encode('utf-8')
                    
                        soup1 = Soup(page1,'html.parser')
                        table1 = soup1.findAll("td", { "id" : "269" })
                        
                        code_link = table1[0].find("a",href=True)
                        #print code_link
                        bill_link = code_link.get('href')
                        bill_link =  bill_link.split("text")[0] +"all-actions"
                        #print "exit"
                        #time.sleep(10)
                        browser.get(bill_link)
                        
                        time.sleep(10)
                        page2 = browser.page_source.encode('utf-8')
                    
                        soup2 = Soup(page2,'html.parser')
                        
                        table2 = soup2.findAll("table", { "class" : "item_table" })
                        #print table2
                        td = soup2.findAll("td",{ "class" : "actions" })
                        #print "td",td
                        #print "one"
                        flag =0
                        for t1 in td:
                            #print t1
                            report_link = t1.find("a",href=True)
                            if report_link is not None:
                                #print report_link.text
                                #print report_link
                                #print report_link.text.find("Rept")
                                if report_link.text.find("Rept") != -1 :
                                    flag= 1
                                    print "Link to the Report  = https://www.congress.gov",report_link.get('href')
                        if flag==0:
                            print "No Report Found"
                            
                        
                #print "after"
                
                
                    #data = [['Me', 'You'],                    ['293', '219'],                    ['54', '13']]
                '''
                a.writerows(info)
                rowcounter+=1
                print "rowcounter",rowcounter
                tests = "a"
                print tests
                print "before search",search
                newsearch = search+"?page="+str(rowcounter)

                print "search ",newsearch
                #webdriver.close()
                #browser.close()
                browser.get(newsearch)
                '''
            #co = 0
            '''
            for l in links:

                #while co<10:
                print "linkss =  ",l
                co =co +1
            '''
            '''
            oid = soup.find("ol",{"id":"stream-items-id"})
            #print oid
            #tid = soup.find("ol",{"id":"headline"}).findAll("li",{"class":"title"}).text.encode('utf-8','replace')
            count = 0
            tid = oid.findAll("li")
            for l in tid:

                tid= l.get("data-item-id")
                lid = l.get("id")
                #print l
                print (tid)
                print (lid)
                if tid is None:
                    pass
                else:
                    count = count +1
                #print l.get("")
            print ("no of tweets :",count)
            '''               
                
       
           
    except ValueError:
        print ("Error")
        print (traceback.format_exc())

    


        

open_browser()