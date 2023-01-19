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


browser = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=option)
browser.get("https://www.google.com")
print(browser.title)
