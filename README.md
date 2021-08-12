# tricount-scraper
As the name suggests.

## Requirements
Install [Chrome WebDriver](https://chromedriver.chromium.org/getting-started) and Python dependencies.

Commands for MacOS setup:
```sh
brew install chromedriver
xattr -d com.apple.quarantine /usr/local/bin/chromedriver

pip3 install -r requirements.txt
```

## Usage
```sh
TRICOUNT_URL=https://tricount.com/en/abcdefghijklm USER_NAME=user LOGLEVEL=20 ./get_payments.py
```

```sh
TRICOUNT_URL=https://tricount.com/en/abcdefghijklm USER_NAME=user EXPENSE_DATE=01/01/2021 EXPENSE_DESCRIPTION='Test expense' EXPENSE_AMOUNT='9.99' ./put_payments.py
```