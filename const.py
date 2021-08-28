from logging import INFO
from os import getenv
from selenium.webdriver.common.by import By

TRICOUNT_URL = getenv('TRICOUNT_URL', default='')
USER_NAME = getenv('USER_NAME', default='')
LOGLEVEL = getenv("LOGLEVEL", default=INFO)
EXPENSE_DESCRIPTION = getenv('EXPENSE_DESCRIPTION', default='')
EXPENSE_AMOUNT = getenv('EXPENSE_AMOUNT', default='')
EXPENSE_DATE = getenv('EXPENSE_DATE', default='')

#PAYED_FOR_ ...TBD: for now the defeult is All
SAVE_PAYMENT_XPATH = '//*[@id="slot1"]/table/tbody/tr[5]/td/div/table/tbody/tr/td/table/tbody/tr/td[1]/a'
PAYMENT_AMOUNT_XPATH = '//*[@id="slot1"]/table/tbody/tr[4]/td/table/tbody/tr/td[2]/div/div/div/table/tbody/tr[4]/td/table/tbody/tr/td[1]/table/tbody/tr/td[2]/input'
PAYMENT_DATE_XPATH = '//*[@id="slot1"]/table/tbody/tr[4]/td/table/tbody/tr/td[2]/div/div/div/table/tbody/tr[3]/td/table/tbody/tr/td[1]/table/tbody/tr/td[2]/input'
PAYER_DD_XPATH = '//*[@id="slot1"]/table/tbody/tr[4]/td/table/tbody/tr/td[2]/div/div/div/table/tbody/tr[2]/td/table/tbody/tr/td[1]/table/tbody/tr/td[2]/select'
PAYMENT_DESCRIPTION_XPATH = '//*[@id="slot1"]/table/tbody/tr[4]/td/table/tbody/tr/td[2]/div/div/div/table/tbody/tr[1]/td/table/tbody/tr/td[1]/table/tbody/tr/td[2]/input'
ADD_EXPENSE_XPATH = '//*[@id="slot1"]/table/tbody/tr[5]/td/div/table/tbody/tr/td/table/tbody/tr/td/a'
USER_XPATH = f'//*[@id="slot1"]/table/tbody/tr[4]/td/table/tbody/tr/td[2]/div/table/tbody/tr/td[1]/div/div/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[2]/div/div/div[text()="{USER_NAME}"]'
IFRAME_ID = 'module-web'
PAYMENTS_TABLE_XPATH = '//*[@id="slot1"]/table/tbody/tr[4]/td/table/tbody/tr/td[2]/div/div/div/table'
PAYMENTS_TABLE_CLASS = 'paymentPanel'
EXPENSES_DIVS_XPATH = '//div[@class="paymentListContent"]|//a[@class="paymentListContent"]' # mix of div and a
DRIVER_WAIT_TIMEOUT = 10

PAGE_NAV_ORDER = [
    "pre_users_list",
    "users_list",
    "expenses_list",
    "expense_form",
    "invalid_url",
]
ELEMENTS_PER_PAGE = {
    "pre_users_list": {"locator": By.ID,    "element": IFRAME_ID},
    "users_list":     {"locator": By.XPATH, "element": USER_XPATH},
    "expenses_list":  {"locator": By.XPATH, "element": ADD_EXPENSE_XPATH},
    "expense_form":   {"locator": By.XPATH, "element": SAVE_PAYMENT_XPATH},
}