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
from const import *

import logging
logging.basicConfig(level=int(LOGLEVEL))

# prevent bot detection
webdriver_options = ChromeOptions()
webdriver_options.add_argument("--headless")  
webdriver_options.add_experimental_option("excludeSwitches", ["enable-automation"])
webdriver_options.add_experimental_option('useAutomationExtension', False)

logging.info(f"Working on expense {EXPENSE_DESCRIPTION} - {EXPENSE_AMOUNT} by {USER_NAME} on {EXPENSE_DATE}.")

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
        WebDriverWait(driver, DRIVER_WAIT_TIMEOUT).until(
            EC.presence_of_element_located((By.XPATH, USER_XPATH))
        )
        driver.find_element_by_xpath(USER_XPATH).click()

        logging.info(f"Waiting the button 'Add an expense' to load.")
        WebDriverWait(driver, DRIVER_WAIT_TIMEOUT).until(
            EC.presence_of_element_located((By.XPATH, ADD_EXPENSE_XPATH))
        )
        driver.find_element_by_xpath(ADD_EXPENSE_XPATH).click()
    except TimeoutException:
        logging.exception(f"Timeout expired, exiting.")
        exit(1)
    else:
        logging.info("Successfully loaded.")
    
    try:
        logging.info(f"Filling out expense form for user {USER_NAME}")
        text_box = driver.find_element_by_xpath(PAYMENT_DESCRIPTION_XPATH)
        text_box.send_keys(EXPENSE_DESCRIPTION)
        text_box = driver.find_element_by_xpath(PAYMENT_DATE_XPATH)
        text_box.send_keys(EXPENSE_DATE)
        text_box = driver.find_element_by_xpath(PAYMENT_AMOUNT_XPATH)
        text_box.send_keys(EXPENSE_AMOUNT)
    except Exception as e:
        logging.exception(f"Failed filling out the expense form.")

    try:
        logging.info(f"Saving the payment.")
        driver.find_element_by_xpath(SAVE_PAYMENT_XPATH).click()
    except Exception as e:
        logging.exception("Failed saving payment.")

