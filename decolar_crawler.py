#!/usr/bin/env python3

import json
import time

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


browser = webdriver.Chrome()

# Decolar home
browser.get('https://www.decolar.com/passagens-aereas')

time.sleep(2)
(browser.find_element_by_css_selector('span[class*="eva-close"]')
 .click())

origin = (browser.find_element_by_class_name('searchbox-sbox-all-boxes')
          .find_element_by_css_selector('div[class*="sbox-origin-container"]')
          .find_element_by_css_selector('input[class*="origin-input"]'))
origin.clear()
origin.send_keys('São Paulo, Brasil')

time.sleep(1)

(browser.find_element_by_class_name('searchbox-sbox-all-boxes')
 .find_element_by_css_selector('div[class*="sbox-origin-container"]')
 .find_element_by_css_selector('ul[class="geo-autocomplete-list"]')
 .find_element_by_css_selector('a[href="#"]')
 .click())


destination = (browser.find_element_by_class_name('searchbox-sbox-all-boxes')
               .find_element_by_css_selector('div[class*="sbox-destination-container"]')
               .find_element_by_css_selector('input[class*="destination-input"]'))
destination.clear()
destination.send_keys('Toronto, Canadá')

time.sleep(1)

(browser.find_element_by_class_name('searchbox-sbox-all-boxes')
 .find_element_by_css_selector('div[class*="sbox-destination-container"]')
 .find_element_by_css_selector('ul[class="geo-autocomplete-list"]')
 .find_element_by_css_selector('a[href="#"]')
 .click())

(browser.find_element_by_class_name('searchbox-sbox-all-boxes')
 .find_element_by_css_selector('input[class*="sbox-bind-checked-no-specified-date"]')
 .send_keys(Keys.SPACE))

# Close elements that will fuck up
(browser.find_element_by_class_name('searchbox-sbox-all-boxes')
 .find_element_by_css_selector('a[class*="sbox-search')
 .click())

time.sleep(5)

results = list()
for cluster in browser.find_elements_by_css_selector('div[class*="flights-cluster"]'):
    currency = cluster.find_element_by_css_selector('span[class*="price-mask"]').text
    total_amount = (cluster.find_element_by_css_selector('span[class*="price-amount"]').text
                    .replace(',', '').replace('.', ''))

    cluster_dict = {
        'currency': currency,
        'total_amount': total_amount,
    }

    for subcluster in cluster.find_elements_by_class_name('sub-cluster'):
        route_type = subcluster.find_element_by_css_selector('route-info-item[itemtype="type"]').text

        day = subcluster.find_element_by_class_name('day').text
        month_year = subcluster.find_element_by_class_name('month-and-year').text

        departure = subcluster.find_element_by_css_selector('span[class*="route-departure-location"]')
        departure_airport = departure.find_element_by_css_selector('span[class*="airport"]').text
        departure_city = departure.find_element_by_css_selector('span[class*="city-departure"]').text
        departure_time = subcluster.find_element_by_css_selector('itinerary-element[class="leave"]').text

        stops = subcluster.find_element_by_css_selector('itinerary-element[class="stops"]').text
        stops = [int(s) for s in stops if s.isdigit()][0]

        arrival = subcluster.find_element_by_css_selector('span[class*="route-arrival-location"]')
        arrival_airport = arrival.find_element_by_css_selector('span[class*="airport"]').text
        arrival_city = arrival.find_element_by_css_selector('span[class*="city-arrival"]').text

        arrive = subcluster.find_element_by_css_selector('itinerary-element[class="arrive"]')
        arrive_time = arrive.find_element_by_class_name('hour').text

        days_difference = arrive.find_element_by_class_name('days-difference').text
        days_difference = [int(s) for s in days_difference if s.isdigit()][0]

        total_time = subcluster.find_element_by_css_selector('itinerary-element[class="time"]').text

        cluster_dict[route_type.lower()] = {
            'date': day + ' ' + month_year,
            'departure': {
                'airport': departure_airport,
                'city': departure_city,
                'time': departure_time,
            },
            'stops': stops,
            'arrival': {
                'airport': arrival_airport,
                'city': arrival_city,
                'time': arrive_time,
                'days_difference': days_difference,
            },
            'total_time': total_time
        }

    results.append(cluster_dict)

browser.quit()

with open('results.json', 'w') as output:
    json.dump(results, output, ensure_ascii=False, indent=2)

