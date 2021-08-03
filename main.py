#!/usr/bin/env python3

from bs4 import BeautifulSoup
from lxml import  html
from math import floor
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from const import LOGLEVEL, TRICOUNT_URL, USER_NAME, USER_XPATH,IFRAME_ID, PAYMENTS_TABLE_CLASS, EXPENSES_DIVS_XPATH, DRIVER_WAIT_TIMEOUT

import logging
logging.basicConfig(level=int(LOGLEVEL))

# prevent bot detection
webdriver_options = ChromeOptions()
webdriver_options.add_argument("--headless")  
webdriver_options.add_experimental_option("excludeSwitches", ["enable-automation"])
webdriver_options.add_experimental_option('useAutomationExtension', False)

payments = []

with webdriver.Chrome('chromedriver', options=webdriver_options) as driver:
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    driver.get(url=TRICOUNT_URL)

    try:
        logging.info(f"Waiting the iframe {IFRAME_ID} to load.")
        result = WebDriverWait(driver, DRIVER_WAIT_TIMEOUT).until(
            EC.presence_of_element_located((By.ID, IFRAME_ID))
        )
    except TimeoutException:
        logging.exception(f"Timeout expired, iframe {IFRAME_ID} not loaded, exiting.")
        exit(1)

    logging.info(f"Switching to iframe {IFRAME_ID}.") 
    driver.switch_to.frame(driver.find_element_by_id(IFRAME_ID))

    # navigate to user's expenses
    try:
        logging.info(f"Waiting the button {USER_NAME} to load.")
        result = WebDriverWait(driver, DRIVER_WAIT_TIMEOUT).until(
            EC.presence_of_element_located((By.XPATH, USER_XPATH))
        )
        driver.find_element_by_xpath(USER_XPATH).click()
    except TimeoutException:
        logging.exception(f"Timeout expired, button {USER_NAME} not loaded, exiting.")
        exit(1)

    parsed_page = BeautifulSoup(driver.page_source,'html.parser')

    # potentially this one can be skipped
    try:
        logging.info("Looking for payments table.")
        table = parsed_page.find_all("table", {"class": PAYMENTS_TABLE_CLASS})[0]
    except IndexError:
        logging.exception("Payments table not found, exiting.")
        exit(1)
    
    tree = html.fromstring(str(parsed_page))
    div_list = tree.xpath(EXPENSES_DIVS_XPATH)
    
    try:
        logging.info("Validating expense fields list.")
        assert len(div_list) % 6 == 0
    except AssertionError:
        logging.exception("Expected multiple of 6. Some expenses might fail to be parsed.")
    else:
        logging.info(f"Retreived {len(div_list)} expense fields to be parsed.")


    d_idx = 0
    while d_idx < len(div_list):
        payment_num = floor((d_idx) / 6)
        logging.debug(f"Parsing payment entry n. {payment_num}.")

        try:
            # TO DO validate fields
            payments.append(
                {
                    'payer_name':         div_list[d_idx + 0].xpath('text()')[0],
                    'paid_amount':        div_list[d_idx + 1].xpath('text()')[0],
                    'payment_date':       div_list[d_idx + 2].xpath('text()')[0],
                    'person_involved':    div_list[d_idx + 3].xpath('text()')[0],
                    'current_users_part': div_list[d_idx + 4].xpath('text()')[0],
                }
            )
        except Exception as e:
            logging.exception(f"Something bad happened while parsing payment n. {payment_num}.", e)
            break
        else:
            d_idx += 6

logging.info(f"Payments retrieved: {len(payments)}")
logging.info(f"{payments}")
