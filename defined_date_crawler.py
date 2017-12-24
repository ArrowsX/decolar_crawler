#!/usr/bin/env python3

import time
import datetime as dt 

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


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


org = 'SAO'
dest = 'YTO'
n_people = 2

for i in range(23):
    start_date = (dt.date(2018, 1, 1) + dt.timedelta(days=i)).strftime('%Y-%m-%d')
    end_date = (dt.date(2018, 1, 9) + dt.timedelta(days=i)).strftime('%Y-%m-%d')

    driver = webdriver.Chrome()

    driver.get('https://www.decolar.com/shop/flights/results/roundtrip/{0}/{1}/{2}/{3}/{4}/0/0?from=SB'.format(
        org, dest, start_date, end_date, n_people
    ))
    time.sleep(20)

    matrix = driver.find_element_by_class_name('matrix-container')

    scales = (driver.find_element_by_css_selector('ul[class="matrix-scales"]')
              .find_elements_by_css_selector('li[class*="scale"]'))
    for scale in scales[1:]:
        print(scale.get_attribute('innerHTML').strip())

    driver.close()
    break
