from time import sleep, strftime
from random import randint
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import smtplib
from email.mime.multipart import MIMEMultipart

chromedriver_path = '/usr/local/bin/chromedriver'

option = webdriver.ChromeOptions()

option.binary_location = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'


browser = webdriver.Chrome(executable_path=chromedriver_path, options=option)


kayak = 'https://www.kayak.com/flights/OSA-SAN/2023-02-17-flexible-3days/2023-02-24-flexible-3days?'

browser.get(kayak)

cheap_results = '//a[@data-code ="price"]'
browser.find_element("xpath", cheap_results).click()
sleep(3)

xp_results_table = '//*[@class = "resultWrapper"]'
flight_containers = browser.find_elements("xpath", xp_results_table)
flights_list = [flight.text for flight in flight_containers]

print(flights_list)


# FUNCTIONS

# function to load more results
def load_more():
    try:
        more_results = '//a[@class = "moreButton"'
        browser.find_element('xpath', more_results).click()
        print('sleeping.....')
        sleep(randint(45,60))
    except:
        pass

# Function to take care of scraping
def page_scrape():
    xp_sections = '//[@class="section duration"]'
    sections = browser.find_elements('xpath', xp_sections)
    sections_list = [value.text for value in sections]
    section_outbound_list = sections_list[::2] # separates the flights
    section_return_list = sections_list[1::2] #separates the flights

    if section_a_list ==[]:
        raise SystemExit

    outbound_duration = []
    outbound_section_names = []

    for n in section_outbound_list:
        outbound_section_names.append(''.join(n.split()[2:5]))
        outbound_duration.append(''.join(n.split()[0:2]))

    return_duration = []
    return_section_names = []

    for n in section_return_list:
        return_section_names.append(''.join(n.split()[2:5]))
        return_duration.append(''.join(n.split()[0:2]))

    xp_dates = '//div[@class="section date"]'
    dates = browser.find_element('xpath', xp_dates)
    dates_list = [value.text for value in dates]
    outbound_date_list = dates_list[::2]
    return_date_list = dates_list[1::2]

    # Separating weekeday from day
    outbound_day = [value.split()[0] for value in outbound_date_list]
    outbound_weekday = [value.split()[0] for value in outbound_date_list]
    return_day = [value.split()[0] for value in return_date_list]
    return_weekday = [value.split()[0] for value in return_date_list]
