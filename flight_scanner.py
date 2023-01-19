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

    # getting prices
    xp_prices = '//a[@class="booking-link"/span[@class="price option-text"]'
    prices = browser.find_elements("xpath", xp_prices)
    # MAY NEED TO REPLACE DOLLAR WITH YEN SIGN
    prices_list = [price.text.replace('$', '') for price in prices if price.text != '']

    prices_list = list(map(int, prices_list))

    xp_stops = '//div[@class="section stops"]/div[1]'
    stops = browser.find_elements("xpath", xp_stops)
    stops_list = [stop.text[0].replace('n', '0') for stop in stops]
    outbound_stop_list = stops_list[::2]
    return_stop_list = stops_list[1::2]

    xp_stops_cities = '//div[@class="section stops"]/div[2]'
    stops_cities = browser.find_elements("xpath", xp_stops_cities)
    stops_cities_list = [stop.text for stop in stops_cities]
    outbound_stop_name_list = stops_cities_list[::2]
    return_stop_name_list = stops_cities_list[1::2]

    # gets the airline company and departure / arrival times for outbound and inbound

    xp_schedule = '//div[@class="section times"]'
    schedules = browser.find_elements("xpath", xp_schedule)
    hours_list = []
    carrier_list = []
    for schedule in schedules:
        hours_list.append(schedule.text.split('\n')[0])
        carrier_list.append(schedule.text.split('\n')[1])
    outbound_hours = hours_list[::2]
    outbound_carrier = carrier_list[::2]
    return_hours = hours_list[1::2]
    return_carrier = carrier_list[1::2]

    cols = (['Out Day', 'Out Time', 'Out Weekday', 'Out Airline', 'Out Cities', 'Out Duration', 'Out Stops', 'Out Stop Cities', 'Return Day', 'Return Time', 'Return Weekday', 'Return Airline', 'Return Cities', 'Return Duration', 'Return Stops', 'Return Stop Cities', 'Price'])

    flights_df = pd.DataFrame({
        'Out Day': outbound_day,
        'Out Weekday': outbound_weekday,
        'Out Duration': outbound_duration,
        'Out Cities': outbound_section_names,
        'Return Day': return_day,
        'Return Weekday': return_weekday,
        'Return Duration': return_duration,
        'Return Cities': return_section_names,
        'Out Stops': outbound_stop_list,
        'Out Stop Cities': outbound_stop_name_list,
        'Return Stops': return_stop_list,
        'Return Stop Cities': return_stop_name_list,
        'Out Time': outbound_carrier,
        'Out Airline': outbound_carrier,
        'Return Time': return_hours,
        'Return Airline': return_carrier,
        'Price': prices_list
    })[cols]

    flights_df['timestamp'] = strftime("%Y%m%d-%H%M")

    return flights_df
