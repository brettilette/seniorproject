# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 11:42:30 2018

@author: Chand
"""

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from random import randint
from time import sleep
from secrets import *
import pandas as pd
import requests
import bs4

def glassdoor_reviews(company):
    
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=options)
    
    # SIGN IN/INITIALIZE
    browser.get("https://www.glassdoor.com/profile/login_input.htm?userOriginHook=HEADER_SIGNIN_LINK")
    browser.find_element_by_name('username').send_keys("j3525535@nwytg.net") # SECRETS
    browser.find_element_by_name('password').send_keys("Q!W@E#R$T%") # SECRETS
    browser.find_element_by_name('password').send_keys(Keys.RETURN)
    sleep(randint(3,5))
    print("Sign In Successful")
    
    
    # NAVIGATE TO REVIEWS
    browser.get('https://www.glassdoor.com/Reviews/index.htm')
    browser.find_element_by_id('KeywordSearch').send_keys(company)
    browser.find_element_by_id('HeroSearchButton').click()
    browser.execute_script("window.history.go(-1)")
    browser.get('https://www.glassdoor.com/Reviews/index.htm')
    browser.find_element_by_id('KeywordSearch').send_keys(company)
    browser.find_element_by_id('HeroSearchButton').click()
    try: # MAIN CASE - Name matches page exactly
        URL = browser.current_url
        _, URL = URL.split('EI_I')
        Code = URL.split('.')[0]
        browser.get('https://www.glassdoor.com/Reviews/' + company.replace(' ', '-') + '-Reviews-' + Code + '.htm')
    except: # POSSIBLE CASE - Need to select the correct page (assumes 1st)
        browser.find_element_by_link_text('See all Reviews').click()
        URL = browser.current_url
        _, URL = URL.split('EI_I')
        Code = URL.split('.')[0]
        browser.get('https://www.glassdoor.com/Reviews/' + company.replace(' ', '-') + '-Reviews-' + Code + '.htm')
    
    # PULLING REVIEWS
    # TODO: Add functionality for more pages
    print("Gathering Reviews...")
    pros = []
    cons = []
    for i in range(len(browser.find_elements_by_class_name('pros'))):
        print('\t' + str(i))
        pros.append(browser.find_elements_by_class_name('pros')[i].text)
        cons.append(browser.find_elements_by_class_name('cons')[i].text)
    print("Done!")
    
    browser.close()    
    return pd.DataFrame({'Pros': pros, 'Cons': cons}).to_json(orient='records')