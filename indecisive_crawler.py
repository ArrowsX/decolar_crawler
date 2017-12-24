#!/usr/bin/env python3

import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


browser = webdriver.Chrome()

# Decolar home
browser.get('https://www.decolar.com/passagens-aereas')

time.sleep(2)
(browser
 .find_element_by_css_selector('span[class*="eva-close"]')
 .click())

search_container = browser.find_element_by_class_name('searchbox-sbox-all-boxes')

origin = (search_container
          .find_element_by_css_selector('div[class*="sbox-origin-container"]')
          .find_element_by_css_selector('input[class*="origin-input"]'))
origin.clear()
origin.send_keys('São Paulo, Brasil')

time.sleep(1)

(search_container
 .find_element_by_css_selector('div[class*="sbox-origin-container"]')
 .find_element_by_css_selector('ul[class="geo-autocomplete-list"]')
 .find_element_by_css_selector('a[href="#"]')
 .click())


destination = (search_container
               .find_element_by_css_selector('div[class*="sbox-destination-container"]')
               .find_element_by_css_selector('input[class*="destination-input"]'))
destination.clear()
destination.send_keys('Toronto, Canadá')

time.sleep(1)

(search_container
 .find_element_by_css_selector('div[class*="sbox-destination-container"]')
 .find_element_by_css_selector('ul[class="geo-autocomplete-list"]')
 .find_element_by_css_selector('a[href="#"]')
 .click())

(search_container
 .find_element_by_css_selector('input[class*="sbox-bind-checked-no-specified-date"]')
 .send_keys(Keys.SPACE))

# Close elements that will fuck up
(search_container
 .find_element_by_css_selector('a[class*="sbox-search')
 .click())

time.sleep(10)
browser.quit()
