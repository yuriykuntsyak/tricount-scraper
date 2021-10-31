# tricount-cli
Unofficial cli client to interact with [tricount.com](https://tricount.com).

Developed in response of unavailability of Tricount's API for public use.

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
File `expenses.csv` should follow the following format:
```csv
date;amount;description;payer_name;paid_for_user
1/1/2021;1.1;test payment 1;user1;all
1/1/2021;2.45;test payment 2;user2;user1
1/1/2021;10.0;test payment 3;user2;user1,user3
```

Run the script:
```sh
usage: main.py [-h] [-u TRICOUNT_URL] [-n USERNAME] [-f FILE_PATH] [-l {CRITICAL,ERROR,WARNING,INFO,DEBUG}] [-c {True,False}]

tricount-cli - Unofficial CLI for tricount.com

optional arguments:
  -h, --help            show this help message and exit
  -u TRICOUNT_URL, --url TRICOUNT_URL
                        URL to your Tricount. Format: 'https://tricount.com/en/abcdefgihjklm' (default: None)
  -n USERNAME, --username USERNAME
                        Your username on Tricount. (default: None)
  -f FILE_PATH, --file-path FILE_PATH
                        Path to the CSV file. (default: ./expenses.csv)
  -l {CRITICAL,ERROR,WARNING,INFO,DEBUG}, --log-level {CRITICAL,ERROR,WARNING,INFO,DEBUG}
                        Set log level. (default: INFO)
  -c {True,False}, --check-submission {True,False}
                        Verify each entry after submission. (default: True)

Reads expense entries from CSV and submits them to tricount.com.
```
