#!/usr/bin/env python3

import argparse
import csv
import logging

from bs4 import BeautifulSoup
from lxml import html  # nosec - should replace with defusedxml equivalent
from math import floor
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep

from const import (
    ADD_EXPENSE_XPATH,
    DRIVER_WAIT_TIMEOUT,
    EXPENSES_DIVS_XPATH,
    IFRAME_ID,
    PAGE_NAV_ORDER,
    PAYMENT_AMOUNT_XPATH,
    PAYMENT_DATE_XPATH,
    PAYMENT_DESCRIPTION_XPATH,
    PAYMENTS_TABLE_XPATH,
    SAVE_PAYMENT_XPATH,
    USERS_LIST_XPATH,
    ELEMENTS_PER_PAGE,
)


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
        super().__init__(
            "Current URL is not valid. Expected "
            f"'.*{self.expected_url}.*', got '{self.current_url}'."
        )


class InvalidPageError(Exception):
    """Page not recognized."""

    def __init__(self):
        super().__init__("Current page is not recognized.")


def wait_for_elements_presence(
    webdriver: webdriver,
    locator,
    elements_list: list,
    elements_description: str = "",
    wait_timeout: int = DRIVER_WAIT_TIMEOUT,
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
                expected_conditions.presence_of_element_located((locator, element))
            )
        except TimeoutException:
            raise ElementNotLoadedError(elements_description)


def is_on_pre_users_list(webdriver: webdriver) -> bool:
    """Making sure we the user list is actually loaded."""
    try:
        wait_for_elements_presence(
            webdriver,
            locator=By.ID,
            elements_list=[IFRAME_ID],
            elements_description="pre user list",
        )
    except ElementNotLoadedError:
        return False
    return True


def is_on_users_list(webdriver: webdriver) -> bool:
    """Making sure we the user list is actually loaded."""
    try:
        wait_for_elements_presence(
            webdriver,
            locator=By.XPATH,
            elements_list=[USERS_LIST_XPATH],
            elements_description="user list",
        )
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
            elements_description="expenses list",
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
            # wait_timeout=20
        )
    except ElementNotLoadedError:
        return False
    return True


def open_link(webdriver: webdriver, link_xpath: str) -> None:
    """
    Find the link by it's xpath and performs a mouse click.
    """
    webdriver.find_element(By.XPATH, link_xpath).click()


def current_page_name(webdriver: webdriver, valid_url: str = "tricount.com") -> str:
    """
    Checks current page for content, determines name.

    Returns:
        page name, according to names in PAGE_NAV_ORDER
    Raises:
        AssertionError - webdriver.current_url doesn't match expected valid_url
        IndexError - none of the expected elements retrieved
    """
    logging.debug(
        "current_page_name: validating webdriver.current_url "
        f"'{webdriver.current_url}' against '{valid_url}'"
    )
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


def browse_to(webdriver: webdriver, url: str, page_name: str, nav_steps_limit: int = 10) -> bool:
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
            locator = ELEMENTS_PER_PAGE[current_page]["locator"]

            logging.debug("browse_to: navigating to next page...")
            wait_for_elements_presence(
                webdriver,
                locator=locator,
                elements_list=elements,
                elements_description=current_page,
                wait_timeout=15,
            )
            open_link(webdriver, elements[0])

        else:
            # browse to initial page
            logging.debug(f"browse_to: running HTTP GET {url}")
            webdriver.get(url=url)
            logging.debug("browse_to: ensuring iframe is loaded")
            wait_for_elements_presence(
                webdriver, locator=By.ID, elements_list=[IFRAME_ID], elements_description="iframe"
            )
            logging.debug(f"browse_to: Switching to iframe {IFRAME_ID}.")
            webdriver.switch_to.frame(webdriver.find_element(By.ID, IFRAME_ID))

            logging.debug("browse_to: Navigating to expense list for user.")
            if not is_on_users_list(webdriver):
                logging.error("browse_to: failed loading users list page.")

        return browse_to(
            webdriver, url=url, page_name=page_name, nav_steps_limit=nav_steps_limit - 1
        )


def fill_textbox(webdriver: webdriver, text_xpath: str, text_content: str) -> None:
    """Fills out a text box located by xpath."""
    webdriver.find_element(By.XPATH, text_xpath).send_keys(text_content)


def get_user_list(webdriver: webdriver, url: str) -> list:
    """Gets list of users from users_list page."""
    users = []
    users_xpath = '//*[@id="slot1"]/table/tbody/tr[4]/td/table/tbody/tr/td[2]/div/table/tbody/tr/td[1]/div/div/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[2]/div/div/div'  # noqa

    if not browse_to(webdriver, url=url, page_name="users_list"):
        logging.error("Something wrong happened while navigating to users_list.")

    logging.debug("get_user_list: parsing users_list page")
    parsed_page = BeautifulSoup(webdriver.page_source, "html.parser")
    tree = html.fromstring(str(parsed_page))
    div_list = tree.xpath(users_xpath)

    for div in div_list:
        user = div.xpath("text()")[0]
        logging.debug(f"get_user_list: adding user {user}.")
        users.append(user)

    return users


def submit_expense(
    webdriver: webdriver,
    url: str,
    description: str,
    amount: str,
    date: str,
    payer_name: str = "",  # unused
    paid_for_user: str = "all",
    available_users: list = [],
) -> None:
    """Submits one expense."""
    logging.info(
        "Initiating expense submission: "
        f"[{description}][{amount}][{date}][{payer_name}][{paid_for_user}]."
    )

    browse_to(webdriver, url=url, page_name="expense_form")

    if not browse_to(webdriver, url=url, page_name="expense_form"):
        logging.error(
            "Failed browsing to expense_form. "
            "Exiting. Failed initiating expense submission: "
            f"[{description}][{amount}][{date}][{payer_name}][{paid_for_user}]."
        )
        sleep(10)
        exit(1)

    try:
        logging.debug("Filling out expense form.")
        fill_textbox(webdriver, text_xpath=PAYMENT_DESCRIPTION_XPATH, text_content=description)
        fill_textbox(webdriver, text_xpath=PAYMENT_DATE_XPATH, text_content=date)
        fill_textbox(webdriver, text_xpath=PAYMENT_AMOUNT_XPATH, text_content=amount)
    except Exception:
        logging.exception("Failed filling out the expense form, skipping expense submission.")
        return

    try:
        if paid_for_user != "all":
            # 'all' is the default selection, no action needed
            logging.debug(f"Selecting paid for user {paid_for_user}")
            paid_for_user_list = paid_for_user.split(",")

            for user in available_users:
                if not (user in paid_for_user_list):
                    logging.debug(f"Deselecting user {user}")
                    open_link(webdriver, f'//div[@class="repartitionNameLabel"][text()="{user}"]')

    except Exception:
        logging.exception("Failed selecting paid_for_user")
        return

    try:
        open_link(webdriver, SAVE_PAYMENT_XPATH)
    except Exception:
        logging.exception("Failed submitting the expense.")
    else:
        logging.debug("Successfully submitted the expense.")


def get_submitted_expenses(webdriver: webdriver, url: str) -> list:
    """Returns list of retrieved expenses"""

    browse_to(webdriver, url=url, page_name="expenses_list"), "Failed browsing to expenses_list."

    payments = []

    parsed_page = BeautifulSoup(webdriver.page_source, "html.parser")
    tree = html.fromstring(str(parsed_page))
    div_list = tree.xpath(EXPENSES_DIVS_XPATH)

    logging.debug("Validating expense fields list.")
    if len(div_list) % 7 != 0:
        logging.error("Expected multiple of 7. Some expenses might fail to be parsed.")
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
                    "payer_name": div_list[d_idx + 0].xpath("text()")[0],
                    "amount": div_list[d_idx + 1].xpath("text()")[0].split(" ")[0],
                    "description": div_list[d_idx + 2].xpath("text()")[0],
                    "date": div_list[d_idx + 3].xpath("text()")[0],
                    "paid_for_user": div_list[d_idx + 4].xpath("text()")[0].split(" ")[0],
                    "current_users_part": div_list[d_idx + 5].xpath("text()")[0],
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
        "day": date.split("/")[0].zfill(2),
        "month": date.split("/")[1].zfill(2),
        "year": date.split("/")[2][-2:],  # only last 2 digits
    }


def is_eq_date(a: str, b: str) -> bool:
    return parse_date_str(a) == parse_date_str(b)


def is_eq_expense(a: dict, b: dict) -> bool:
    """Checks expense equality."""
    return (
        a.get("description", "a") == b.get("description", "b")
        and float(a.get("amount", 0.0)) == float(b.get("amount", 1.1))
        and is_eq_date(a.get("date", "a"), b.get("date", "b"))
        and a.get("payer_name", "a") == b.get("payer_name", "b")
    )


def is_expense_submitted(webdriver: webdriver, url: str, expense: dict) -> bool:
    """Checks if expense is present on submitted expenses page.
    Looks only for the first occurrence. Further tweaking might be required.
    """
    for submitted in get_submitted_expenses(webdriver, url):
        if is_eq_expense(submitted, expense):
            logging.debug(f"is_expense_submitted: found matching expense {expense}.")
            return True
    return False


def get_args():
    parser = argparse.ArgumentParser(
        description="tricount-cli - Unofficial CLI for tricount.com",
        epilog="Reads expense entries from CSV and submits them to tricount.com.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-u",
        "--url",
        dest="tricount_url",
        help="URL to your Tricount. Format: 'https://tricount.com/en/abcdefgihjklm'",
    )

    parser.add_argument("-n", "--username", dest="username", help="Your username on Tricount.")

    parser.add_argument(
        "-f",
        "--file-path",
        dest="file_path",
        default="./expenses.csv",
        help="Path to the CSV file.",
    )

    parser.add_argument(
        "-l",
        "--log-level",
        dest="log_level",
        default="INFO",
        choices=["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"],
        help="Set log level.",
    )

    parser.add_argument(
        "-c",
        "--check-submission",
        dest="check_submission",
        default="True",
        choices=["True", "False"],
        help="Verify each entry after submission.",
    )

    return parser


def main():
    args = get_args().parse_args()

    TRICOUNT_URL = args.tricount_url
    LOGLEVEL = args.log_level

    USER_XPATH = f"//div[@class='gwt-Label identifiezVousUserLabel'][text()='{args.username}']"
    ELEMENTS_PER_PAGE["users_list"]["elements"] = [USER_XPATH]

    check_submission = False if args.check_submission == "False" else True

    logging.basicConfig(level=LOGLEVEL)

    # prevent bot detection
    webdriver_options = ChromeOptions()
    webdriver_options.add_argument("--headless")
    webdriver_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    webdriver_options.add_experimental_option("useAutomationExtension", False)

    with webdriver.Chrome("chromedriver", options=webdriver_options) as driver:
        driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
        logging.debug("Initialized Chrome driver.")

        user_list = get_user_list(driver, url=TRICOUNT_URL)
        if user_list == []:
            logging.error("Failed opening Tricount. Exiting.")
            exit(1)

        with open(args.file_path, newline="") as file:
            logging.debug("Reading csv file.")
            expense_list = csv.DictReader(file, delimiter=";")

            for expense in expense_list:
                input("Press ENTER to proceed with next expense...")

                choice = "n"
                expense_already_submitted = False

                if not check_submission:
                    expense_already_submitted = is_expense_submitted(
                        webdriver=driver, url=TRICOUNT_URL, expense=expense
                    )

                if expense_already_submitted and check_submission:
                    choice = input(
                        f"Expense already found: {expense} " "Confirm re-submission? y/[n] "
                    ).lower()
                if not (expense_already_submitted and check_submission) or choice == "y":
                    submit_expense(
                        webdriver=driver, url=TRICOUNT_URL, **expense, available_users=user_list
                    )

                    if check_submission:
                        if not is_expense_submitted(
                            webdriver=driver, url=TRICOUNT_URL, expense=expense
                        ):
                            logging.error(
                                f"Failed verifying expense {expense} submission, exiting."
                            )
                            exit(1)
                        else:
                            logging.info(f"Confirmed submission of expense {expense}")
                    else:
                        logging.info(f"Expense {expense} submitted, skipped checking.")
                else:
                    logging.info(f"Skipping {expense}")


if __name__ == "__main__":
    main()
