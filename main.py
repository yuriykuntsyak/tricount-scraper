#!/usr/bin/env python3

from bs4 import BeautifulSoup
import csv
from lxml import  html
from math import floor
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException
from const import *

from time import sleep

import logging
logging.basicConfig(level=int(LOGLEVEL))

class ElementNotLoadedError(Exception):
    """Not loaded elements on page."""
    def __init__(self, message="undefined"):
        self.message = message
        super().__init__(f"Failed to load element: {self.message}")
class InvalidUrlError(Exception):
    """Current URL is not valid."""
    def __init__(self, expected_url="undefined", current_url="undefined"):
        self.expected_url = expected_url
        self.current_url = current_url
        super().__init__(f"Current URL is not valid. Expected '.*{self.expected_url}.*', got '{self.current_url}'.")
class InvalidPageError(Exception):
    """Page not recognized."""
    def __init__(self):
        super().__init__(f"Current page is not recognized.")

def wait_for_elements_presence(
        webdriver: webdriver,
        locator,
        elements_list: list,
        elements_description: str = "",
        wait_timeout: int = DRIVER_WAIT_TIMEOUT
    ) -> None:
    """
    Waits for the list of elements to be loaded on the page.

    Args:
        webdriver: instance of selenium.webdriver
        locator: mechanism for locating an element on the page (ex. By.XPATH)
        elements_list: list of elements to locate
        elements_description: description to use when raising ElementNotLoadedError exception
        wait_timeout: time to wait for element to load
    """
    
    for element in elements_list:
        try:
            WebDriverWait(webdriver, timeout=wait_timeout).until(
                expected_conditions.presence_of_element_located(
                    (locator, element)
                )
            )
        except TimeoutException:
            raise ElementNotLoadedError(elements_description)

def is_on_pre_users_list(webdriver: webdriver) -> bool:
    """Making sure we the user list is actually loaded."""
    try:
        wait_for_elements_presence(webdriver, locator=By.ID, elements_list=[IFRAME_ID], elements_description="pre user list")
    except ElementNotLoadedError:
        return False
    return True

def is_on_users_list(webdriver: webdriver) -> bool:
    """Making sure we the user list is actually loaded."""
    try:
        wait_for_elements_presence(webdriver, locator=By.XPATH, elements_list=[USER_XPATH], elements_description="user list")
    except ElementNotLoadedError:
        return False
    return True

def is_on_expenses_list(webdriver: webdriver) -> bool:
    """Making sure we the expenses list is actually loaded."""
    try:
        wait_for_elements_presence(
            webdriver,
            locator=By.XPATH,
            elements_list=[ADD_EXPENSE_XPATH, PAYMENTS_TABLE_XPATH],
            elements_description="expenses list"
        )
    except ElementNotLoadedError:
        return False
    return True

def is_on_expense_form(webdriver: webdriver) -> bool:
    """Making sure we the expense form is actually loaded."""

    try:
        wait_for_elements_presence(
            webdriver,
            locator=By.XPATH,
            elements_list=[SAVE_PAYMENT_XPATH, PAYMENT_AMOUNT_XPATH],
            elements_description="expense form",
            #wait_timeout=20
        )
    except ElementNotLoadedError:
        return False
    return True

def open_link(webdriver: webdriver, link_xpath: str) -> None:
    """
    Find the link by it's xpath and performs a mouse click.
    """
    webdriver.find_element_by_xpath(link_xpath).click()
    
def current_page_name(webdriver: webdriver, valid_url: str = "tricount.com") -> str:
    """
    Checks current page for content, determines name.

    Returns:
        page name, according to names in PAGE_NAV_ORDER
    Raises:
        AssertionError - webdriver.current_url doesn't match expected valid_url
        IndexError - none of the expected elements retrieved
    """
    logging.debug(f"current_page_name: validating webdriver.current_url '{webdriver.current_url}' against '{valid_url}'")
    if webdriver.current_url.find(valid_url) == -1:
        raise InvalidUrlError(expected_url=valid_url, current_url=webdriver.current_url)

    if is_on_expense_form(webdriver):
        return "expense_form"
    elif is_on_expenses_list(webdriver):
        return "expenses_list"
    elif is_on_users_list(webdriver):
        return "users_list"
    elif is_on_pre_users_list(webdriver):
        return "pre_users_list"
    else:
        raise InvalidPageError

def browse_to(webdriver: webdriver, page_name: str, nav_steps_limit: int = 10) -> bool:
    """
    Navigates, by following pages listed in PAGE_NAV_ORDER, until specified page.

    Args:
        webdriver - webdriver
        page_name - name of the page as per PAGE_NAV_ORDER
        nav_steps_limit - max steps per navigation
    Returns:
        bool - indicating if page_name has been reached
    """
    logging.debug(f"browse_to: targeting page {page_name}")
    logging.debug(f"browse_to: webdriver.current_url={webdriver.current_url}")
    logging.debug(f"browse_to: nav_steps_limit={nav_steps_limit}")

    try:
        current_page = current_page_name(webdriver)
    except InvalidUrlError:
        logging.debug("InvalidUrlError while calling current_page_name")
        current_page = "invalid_url"
    except InvalidPageError:
        logging.debug("InvalidPageError while calling current_page_name")
        current_page = "invalid_url"
    finally:
        logging.debug(f"browse_to: current_page={current_page}.")
    
    if current_page == page_name:
        logging.debug(f"browse_to: Completed browsing to {page_name}.")
        return True

    if nav_steps_limit <= 0:
        logging.debug("browse_to: Navigation steps limit reached.")
        return False
    else:
        if PAGE_NAV_ORDER.index(current_page) < PAGE_NAV_ORDER.index(page_name):
            elements = ELEMENTS_PER_PAGE[current_page]["elements"]
            locator  = ELEMENTS_PER_PAGE[current_page]["locator"]

            logging.debug("browse_to: navigating to next page...")
            wait_for_elements_presence(webdriver, locator=locator, elements_list=elements, elements_description=current_page, wait_timeout=15)
            open_link(webdriver, elements[0])

        else:
            # browse to initial page
            logging.debug(f"browse_to: running HTTP GET {TRICOUNT_URL}")
            webdriver.get(url=TRICOUNT_URL)
            logging.debug(f"browse_to: ensuring iframe is loaded")
            wait_for_elements_presence(webdriver, locator=By.ID, elements_list=[IFRAME_ID], elements_description="iframe")
            logging.debug(f"browse_to: Switching to iframe {IFRAME_ID}.") 
            webdriver.switch_to.frame(webdriver.find_element_by_id(IFRAME_ID))

            logging.debug("browse_to: Navigating to expense list for user.")
            if not is_on_users_list(webdriver):
                logging.error("browse_to: failed loading users list page.")
            
        return browse_to(webdriver, page_name=page_name, nav_steps_limit=nav_steps_limit-1)

def fill_textbox(webdriver: webdriver, text_xpath: str, text_content: str) -> None:
    """Fills out a text box located by xpath."""
    webdriver.find_element_by_xpath(text_xpath).send_keys(text_content)

def get_user_list(webdriver: webdriver) -> list:
    """Gets list of users from users_list page."""
    users = []
    users_xpath = '//*[@id="slot1"]/table/tbody/tr[4]/td/table/tbody/tr/td[2]/div/table/tbody/tr/td[1]/div/div/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[2]/div/div/div'
    
    assert browse_to(webdriver, page_name="users_list"), "Something wrong happened while navigating to users_list."

    logging.debug(f"get_user_list: parsing users_list page")
    parsed_page = BeautifulSoup(webdriver.page_source,'html.parser')
    tree = html.fromstring(str(parsed_page))
    div_list = tree.xpath(users_xpath)

    for div in div_list:
        user = div.xpath('text()')[0]
        logging.debug(f"get_user_list: adding user {user}.")
        users.append(user)

    return users

def submit_expense(
        webdriver: webdriver,
        description: str,
        amount: str,
        date: str,
        payer_name: str = "",    # unused
        paid_for_user: str = "all",
        available_users: list = []
    ) -> None:
    """Submits one expense."""
    logging.info(f"Initiating expense submission: [{description}][{amount}][{date}][{payer_name}][{paid_for_user}].")

    browse_to(webdriver, page_name="expense_form")

    try:
        assert browse_to(webdriver, page_name="expense_form"), "Failed browsing to expense_form."
    except AssertionError:
        logging.error(f"Exiting. Failed initiating expense submission: [{description}][{amount}][{date}][{payer_name}][{paid_for_user}].")
        sleep(10)
        exit(1)

    try:
        logging.debug("Filling out expense form.")
        fill_textbox(webdriver, text_xpath=PAYMENT_DESCRIPTION_XPATH, text_content=description)
        fill_textbox(webdriver, text_xpath=PAYMENT_DATE_XPATH, text_content=date)
        fill_textbox(webdriver, text_xpath=PAYMENT_AMOUNT_XPATH, text_content=amount)
    except Exception as e:
        logging.exception(f"Failed filling out the expense form, skipping expense submission.")
        return

    try:
        if paid_for_user != "all":
            # 'all' is the default selection, no action needed
            logging.debug(f"Selecting paid for user {paid_for_user}")
            paid_for_user_list = paid_for_user.split(',')

            for user in available_users:
                if not (user in paid_for_user_list):
                    logging.debug(f"Deselecting user {user}")
                    open_link(webdriver, f'//div[@class="repartitionNameLabel"][text()="{user}"]')

    except Exception as e:
        logging.exception("Failed selecting paid_for_user")
        return

    try:
        open_link(webdriver, SAVE_PAYMENT_XPATH)
    except Exception as e:
        logging.exception("Failed submitting the expense.")
    else:
        logging.debug(f"Successfully submitted the expense.")

def get_submitted_expenses(webdriver: webdriver) -> list:
    """Returns list of retrieved expenses"""

    assert browse_to(webdriver, page_name="expenses_list"), "Failed browsing to expenses_list."

    payments = []

    parsed_page = BeautifulSoup(webdriver.page_source,'html.parser')
    tree = html.fromstring(str(parsed_page))
    div_list = tree.xpath(EXPENSES_DIVS_XPATH)
    
    try:
        logging.debug("Validating expense fields list.")
        assert len(div_list) % 7 == 0
    except AssertionError:
        logging.exception("Expected multiple of 7. Some expenses might fail to be parsed.")
    else:
        logging.debug(f"Retreived {len(div_list)} expense fields to be parsed.")

    d_idx = 0
    while d_idx < len(div_list):
        payment_num = floor((d_idx) / 7)
        logging.debug(f"Parsing payment entry n. {payment_num}.")

        try:
            # TO DO validate fields/values
            #  'myusername','8.00 EUR','aaaa','13/08/21','all','2.67 EUR',',\xa0'
            payments.append(
                {
                    'payer_name':         div_list[d_idx + 0].xpath('text()')[0],
                    'amount':             div_list[d_idx + 1].xpath('text()')[0].split(' ')[0],
                    'description':        div_list[d_idx + 2].xpath('text()')[0],
                    'date':               div_list[d_idx + 3].xpath('text()')[0],
                    'paid_for_user':      div_list[d_idx + 4].xpath('text()')[0].split(' ')[0],
                    'current_users_part': div_list[d_idx + 5].xpath('text()')[0],
                }
            )
        except Exception as e:
            logging.exception(f"Something bad happened while parsing payment n. {payment_num}.", e)
            break
        else:
            d_idx += 7
    return payments

def parse_date_str(date: str) -> dict:
    return {
        "day":   date.split("/")[0].zfill(2),
        "month": date.split("/")[1].zfill(2),
        "year":  date.split("/")[2][-2:] # only last 2 digits
    }

def is_eq_date(a: str, b: str) -> bool:
    return parse_date_str(a) == parse_date_str(b)

def is_eq_expense(a: dict, b: dict) -> bool:
    """Checks expense equality."""
    return (
        a.get("description") == b.get("description")
        and float(a.get("amount")) == float(b.get("amount"))
        and is_eq_date(a.get("date"), b.get("date"))
        and a.get("payer_name")  == b.get("payer_name")
    )

def is_expense_submitted(webdriver: webdriver, expense: dict) -> bool:
    """Checks if expense is present on submitted expenses page.
        Looks only for the first occurrence. Further tweaking might be required.
    """
    for submitted in get_submitted_expenses(webdriver):
        if is_eq_expense(submitted, expense):
            logging.debug(f"is_expense_submitted: found matching expense {expense}.")
            return True
    return False

def main():
    # prevent bot detection
    webdriver_options = ChromeOptions()
    webdriver_options.add_argument("--headless")  
    webdriver_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    webdriver_options.add_experimental_option('useAutomationExtension', False)

    with webdriver.Chrome('chromedriver', options=webdriver_options) as driver:
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        logging.debug(f"Initialized Chrome driver.")

        user_list = get_user_list(driver)
        if user_list == []:
            logging.error("Failed opening Tricount. Exiting.")
            exit(1)

        with open('expenses.csv', newline='') as file:
            logging.debug("Reading csv file.")
            expense_list = csv.DictReader(file, delimiter=';')

            for expense in expense_list:
                input("Press ENTER to proceed with next expense...")

                expense_already_submitted = is_expense_submitted(webdriver=driver, expense=expense)
                choice = "n"

                if expense_already_submitted:
                    choice = input(f"Expense already found: {expense} "
                                   "Confirm re-submission? y/[n] ").lower()
                if (not expense_already_submitted) or choice == "y":
                    submit_expense(webdriver=driver, **expense, available_users=user_list)

                    if not is_expense_submitted(webdriver=driver, expense=expense):
                        logging.error(f"Failed verifying expense {expense} submission, exiting.")
                        exit(1)
                    else:
                        logging.info(f"Confirmed submission of expense {expense}")
                else:
                    logging.info(f"Skipping {expense}")


if __name__ == '__main__':
    main()
