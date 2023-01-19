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
