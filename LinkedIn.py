# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 13:03:23 2018

@author: Chand
"""

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from random import randint
from time import sleep
import pandas as pd
import requests
import bs4
from secrets import *

num_pages = 3 # Hard Coded Number of Pages - This number can be changed in the future based off company size (1 page ~ 10 people)

def google_profile_pull(company_name, num_pages):
    '''
    Scrapes google for the first *pages* pages of results LinkedIn users 
    associated with *company_name* and returns a list of the URLs.
    TODO: Add duplicate removal line using set
    '''
    url_list = []
    print("Now searching Google for " + company_name + " employees...")
    for i in range(0,num_pages):
        sleep(randint(0,5))
        req = requests.get(r'https://www.google.com/search?q=site:linkedin.com/in/ "' + company_name + '"&start=' + str(i) + '0')
        soup = bs4.BeautifulSoup(req.text, 'lxml')
        result = soup.findAll("div",{"class":"g"})
        for j in range(10):
            temp = str(result[j])
            url = str(temp[temp.find('?q=')+3:temp.find('&amp')])
            if(url[0:28] == "https://www.linkedin.com/in/"):
                url_list.append(url)
    print("..." + str(len(url_list)) + " possible employees discovered.")
    return url_list

def linkedin_sign_in(browser):
    '''
    Initializes linkedin browser by logging into fake profile Jimothy Simmons.
    '''
    
    browser.get("https://www.linkedin.com/uas/login?_l=en")
    sleep(randint(2,5))
    
    # New UI Login
    try:
        browser.find_element_by_id("username").send_keys(LINKEDIN_LOGON)
        browser.find_element_by_id("password").send_keys(LINKEDIN_PASS)
        browser.find_element_by_id("password").send_keys(Keys.RETURN)
        sleep(randint(0,5))
        
    # Old UI Login
    except:
        browser.find_element_by_id("session_key-login").send_keys(LINKEDIN_LOGON)
        browser.find_element_by_id("session_password-login").send_keys(LINKEDIN_PASS)
        browser.find_element_by_id("session_password-login").send_keys(Keys.RETURN)
        sleep(randint(0,5))
        
    
def pull_data(browser, url_list, company_name):
    '''
    Iterates over the url_list and pulls a defined set of information from the
    web pages: name (first and last) and company.
    '''
    
    linkedin_sign_in(browser)
    main = []
    
    for i, url in enumerate(url_list):
        job_length = []
        dates_employed = []
        
        try:
            browser.get(url)
            sleep(randint(5,10))
            HTML = browser.page_source
            soup = bs4.BeautifulSoup(HTML, 'lxml')
            
            name = soup.select('h1[class="pv-top-card-section__name inline t-24 t-black t-normal"]')[0].get_text().strip() # Selector Subject to Change
            fname, lname = name.split(" ")           
            company = soup.select('button[class="pv-top-card-v2-section__link pv-top-card-v2-section__link-experience mb1"]')[0].get_text().strip() # Selector Subject to Change
            print(str(i+1) + ". " + fname + " " + lname + " - " + company)
            
            for i in range(5):
                try:
                    job_length.append(str(soup.select('span[class="pv-entity__bullet-item-v2"]')[i].get_text()))
                except:
                    pass
                try:
                    date = str(soup.select('h4[class="pv-entity__date-range t-14 t-black t-normal"]')[i].get_text())
                except:
                    try:
                        date = str(soup.select('h4[class="pv-entity__date-range t-14 t-black--light t-normal"]')[i].get_text())
                    except:
                        pass
                    pass
                date = date.replace('Dates Employed','')
                date = date.strip('\n')
                dates_employed.append(date.replace('Dates Employed',''))
            print(job_length)
            print(dates_employed)
            main.append([url, fname, lname, company, company_name, dates_employed, job_length])
            
        except:
            print(str(i) + ". Mission failed. We'll get em next time: ")
            print("\t" + str(url))

    return pd.DataFrame(main, columns = ['URL', 'FirstName', 'LastName', 'Company', 'SearchedTerm', 'DatesEmployed', 'JobLength'])

def FindEmployees(company):
    url_list = google_profile_pull(company, num_pages)
    
    # Final Version Should Run Headless
# =============================================================================
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=options)
# =============================================================================

    #browser = webdriver.Chrome(CHROMEDRIVER_PATH)
    data = pull_data(browser, url_list, company)
    browser.close()
    return data.to_json(orient='records') 






# =============================================================================
# GET ALL LINKS FROM URL (NON JS)
# aList = []
# for link in soup.findAll('a'):
#     print(link)
#     print("--------------")
# =============================================================================
    
# ITERATE UNTIL IT FAILS?
# =============================================================================
# experience_position_titles = soup.select('h3[class="Sans-17px-black-85%-semibold"]')[0].get_text()
# 
# experience_company = soup.select('h4[class="Sans-17px-black-85%"]')[0].get_text()
# 
# times_spent_at_job = soup.select('span[class="pv-entity__bullet-item-v2"]')[0].get_text()
# =============================================================================
