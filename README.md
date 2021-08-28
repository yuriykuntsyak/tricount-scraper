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

./expenses.csv
```
date,amount,description,payer_name,paid_for_user
1/1/2021,1.1,test payment,myusername,all
```

## Usage
```sh
TRICOUNT_URL=https://tricount.com/en/abcdefghijklm USER_NAME=myusername LOGLEVEL=20 ./main.py
```
