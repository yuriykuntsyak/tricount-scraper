# tricount-cli
Unofficial cli client to interact with [tricount.com](https://tricount.com).

Developed in response of unavailability of tricount's API for public use.

## Features
_TBD_

## Requirements
Install [Chrome WebDriver](https://chromedriver.chromium.org/getting-started) and Python dependencies.

Commands for MacOS setup:
```sh
brew install chromedriver
xattr -d com.apple.quarantine /usr/local/bin/chromedriver

pip3 install -r requirements.txt
```

## Usage
File `./expenses.csv` should follow the following format:
```csv
date;amount;description;payer_name;paid_for_user
1/1/2021;1.1;test payment 1;user1;all
1/1/2021;2.45;test payment 2;user2;user1
1/1/2021;10.0;test payment 3;user2;user1,user3
```

Run the script:
```sh
TRICOUNT_URL=https://tricount.com/en/abcdefghijklm USER_NAME=myusername LOGLEVEL=20 ./main.py
```
