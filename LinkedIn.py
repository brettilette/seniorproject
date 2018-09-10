# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 13:03:23 2018

@author: Chand
"""

from selenium import webdriver
from random import randint
from time import sleep
import pandas as pd
import requests
import bs4

company_name = "Cybriant"
num_pages = 5

def google_profile_pull(company_name, num_pages):
    '''
    Scrapes google for the first *pages* pages of results LinkedIn users 
    associated with *company_name* and returns a list of the URLs.
    '''
    url_list = []
    print("Now searching Google for " + company_name + " employees...")
    for i in range(0,num_pages-1):
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
    Initializes browser by logging into fake profile Jimothy Simmons.
    '''
    browser.get("https://www.linkedin.com/uas/login?_l=en")
    sleep(randint(0,5))
    browser.find_element_by_id("session_key-login").send_keys("phalapel@gmail.com")
    sleep(randint(0,5))
    browser.find_element_by_id("session_password-login").send_keys("Q!W@E#R$T%")
    browser.find_element_by_id("btn-primary").click()
    
def pull_data(browser, url_list, company_name):
    '''
    Iterates over the url_list and pulls a defined set of information from the
    web pages: name (first and last) and company.
    '''
    linkedin_sign_in(browser)
    main = []
    for url in url_list:
        try:
            browser.get(url)
            HTML = browser.page_source
            soup = bs4.BeautifulSoup(HTML, 'lxml')
            name = soup.select('h1[class="pv-top-card-section__name Sans-26px-black-85%"]')[0].get_text().strip()
            fname, lname = name.split(" ")
            company = soup.select('span[class="pv-top-card-v2-section__entity-name pv-top-card-v2-section__company-name text-align-left ml2 Sans-15px-black-85%-semibold lt-line-clamp lt-line-clamp--multi-line ember-view"]')[0].get_text().strip()
            print(fname + " " + lname + " " + company)
            main.append([url, fname, lname, company, company_name])
        except:
            print("Mission failed. We'll get em next time.")

    return pd.DataFrame(main, columns = ['URL', 'FirstName', 'LastName', 'Company', 'Searched Term'])

url_list = google_profile_pull(company_name, num_pages)
browser = webdriver.Chrome()    
data = pull_data(browser, url_list, company_name)
datajson = data.to_json()

# =============================================================================
# GET ALL LINKS FROM URL (NON JS)
# aList = []
# for link in soup.findAll('a'):
#     print(link)
#     print("--------------")
# =============================================================================