from logging import INFO
from os import getenv

TRICOUNT_URL = getenv('TRICOUNT_URL', default='')
USER_NAME = getenv('USER_NAME', default='')
LOGLEVEL = getenv("LOGLEVEL", default=INFO)

USER_XPATH = f'//*[@id="slot1"]/table/tbody/tr[4]/td/table/tbody/tr/td[2]/div/table/tbody/tr/td[1]/div/div/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[2]/div/div/div[text()="{USER_NAME}"]'
IFRAME_ID = 'module-web'
PAYMENTS_TABLE_XPATH = '//*[@id="slot1"]/table/tbody/tr[4]/td/table/tbody/tr/td[2]/div/div/div/table'
PAYMENTS_TABLE_CLASS = 'paymentPanel'
EXPENSES_DIVS_XPATH = '//div[@class="paymentListContent"]'
DRIVER_WAIT_TIMEOUT = 30
