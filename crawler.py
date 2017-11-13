#!/usr/bin/env python3

import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

driver = webdriver.Chrome()


def debug(elem):
    try:
        html_content = elem.get_attribute('outerHTML')
        soup = BeautifulSoup(html_content, 'html.parser')
        print(soup.prettify())
    except AttributeError:
        for x in elem:
            html_content = x.get_attribute('outerHTML')
            soup = BeautifulSoup(html_content, 'html.parser')
            print(soup.prettify())


# Decolar home
driver.get('https://www.decolar.com/passagens-aereas')

time.sleep(2)
popup_close = driver.find_element_by_css_selector('span[class*="eva-close"]')
popup_close.click()

search_container = driver.find_element_by_class_name('searchbox-sbox-all-boxes')

origin_container = search_container.find_element_by_css_selector('div[class*="sbox-origin-container"]')
origin = origin_container.find_element_by_css_selector('input[class*="origin-input"]')
origin.clear()
origin.send_keys('São Paulo, Brasil')
debug(origin)

time.sleep(1)
origin_click = (origin_container
                .find_element_by_css_selector('ul[class="geo-autocomplete-list"]')
                .find_element_by_css_selector('a[href="#"]')
                .click())

destination_container = search_container.find_element_by_css_selector('div[class*="sbox-destination-container"]')
destination = destination_container.find_element_by_css_selector('input[class*="destination-input"]')
destination.clear()
destination.send_keys('Toronto, Canadá')
debug(destination)

time.sleep(1)
dest_click = (destination_container
              .find_element_by_css_selector('ul[class="geo-autocomplete-list"]')
              .find_element_by_css_selector('a[href="#"]')
              .click())

no_specified_date = search_container.find_element_by_css_selector('input[class*="sbox-bind-checked-no-specified-date"]')
no_specified_date.send_keys(Keys.SPACE)
debug(no_specified_date)

# Close elements that will fuck up
search = search_container.find_element_by_css_selector('a[class*="sbox-search')
search.click()

time.sleep(10)
driver.close()
