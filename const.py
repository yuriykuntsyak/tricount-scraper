from selenium.webdriver.common.by import By

DRIVER_WAIT_TIMEOUT = 3

PAID_FOR_USERS = '//div[@class="repartitionNameLabel"]'
SAVE_PAYMENT_XPATH = (
    '//*[@id="slot1"]/table/tbody/tr[5]/td/div/table/tbody/tr/td/table/tbody/tr/td[1]/a'
)
PAYMENT_AMOUNT_XPATH = '//*[@id="slot1"]/table/tbody/tr[4]/td/table/tbody/tr/td[2]/div/div/div/table/tbody/tr[4]/td/table/tbody/tr/td[1]/table/tbody/tr/td[2]/input'  # noqa
PAYMENT_DATE_XPATH = '//*[@id="slot1"]/table/tbody/tr[4]/td/table/tbody/tr/td[2]/div/div/div/table/tbody/tr[3]/td/table/tbody/tr/td[1]/table/tbody/tr/td[2]/input'  # noqa
PAYER_DD_XPATH = '//*[@id="slot1"]/table/tbody/tr[4]/td/table/tbody/tr/td[2]/div/div/div/table/tbody/tr[2]/td/table/tbody/tr/td[1]/table/tbody/tr/td[2]/select'  # noqa
PAYMENT_DESCRIPTION_XPATH = '//*[@id="slot1"]/table/tbody/tr[4]/td/table/tbody/tr/td[2]/div/div/div/table/tbody/tr[1]/td/table/tbody/tr/td[1]/table/tbody/tr/td[2]/input'  # noqa
ADD_EXPENSE_XPATH = (
    '//*[@id="slot1"]/table/tbody/tr[5]/td/div/table/tbody/tr/td/table/tbody/tr/td/a'
)
IFRAME_ID = "module-web"
PAYMENTS_TABLE_XPATH = (
    '//*[@id="slot1"]/table/tbody/tr[4]/td/table/tbody/tr/td[2]/div/div/div/table'
)
PAYMENTS_TABLE_CLASS = "paymentPanel"
EXPENSES_DIVS_XPATH = (
    '//div[@class="paymentListContent"]|//a[@class="paymentListContent"]'  # mix of div and a
)

USERS_LIST_XPATH = (
    '//*[@id="slot1"]/table/tbody/tr[4]/td/table/tbody/tr/td[2]/div/'
    "table/tbody/tr/td[1]/div/div/table/tbody/tr[1]/td/"
    "table/tbody/tr/td/table/tbody/tr/td[2]/div/div/div"
)

ELEMENTS_PER_PAGE = {
    "pre_users_list": {"locator": By.ID, "elements": [IFRAME_ID]},
    "users_list": {"locator": By.XPATH, "elements": []},  # TBD, for now the val is assigned in main
    "expenses_list": {
        "locator": By.XPATH,
        "elements": [ADD_EXPENSE_XPATH, PAYMENTS_TABLE_XPATH],
    },
    "expense_form": {
        "locator": By.XPATH,
        "elements": [SAVE_PAYMENT_XPATH, PAYMENT_AMOUNT_XPATH],
    },
}

PAGE_NAV_ORDER = [
    "pre_users_list",
    "users_list",
    "expenses_list",
    "expense_form",
    "invalid_url",
]
