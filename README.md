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
TRICOUNT_URL=https://tricount.com/en/abcdefghijklm USER_NAME=user LOGLEVEL=20 ./main.py
```
