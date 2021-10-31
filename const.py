from selenium.webdriver.common.by import By

DRIVER_WAIT_TIMEOUT = 3

PAID_FOR_USERS = "//div[@class='repartitionNameLabel']"
SAVE_PAYMENT_XPATH = "//a[@class='footerPanelText'][text()='Save']"
PAYMENT_AMOUNT_XPATH = "//div[@class='inputFieldLabel'][text()='Amount:']/../../td/input"
PAYMENT_DATE_XPATH = "//div[@class='inputFieldLabel'][text()='Date (optional):']/../../td/input"
PAYER_DD_XPATH = "//div[@class='inputFieldLabel'][text()='Who paid?:']/../../td/select"
PAYMENT_DESCRIPTION_XPATH = "//div[@class='inputFieldLabel'][text()='What:']/../../td/input"
ADD_EXPENSE_XPATH = "//a[@class='footerPanelText'][text()='Add an expense']"
IFRAME_ID = "module-web"
PAYMENTS_TABLE_XPATH = "//table[@class='paymentPanel']"
PAYMENTS_TABLE_CLASS = "paymentPanel"
EXPENSES_DIVS_XPATH = "//div[@class='paymentListContent']|//a[@class='paymentListContent']"
USERS_LIST_XPATH = "//div[@class='gwt-Label identifiezVousUserLabel']"

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
