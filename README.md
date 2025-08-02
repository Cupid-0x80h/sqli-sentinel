# SQLi Sentinel - A Simple SQL Injection Scanner

SQLi Sentinel is a command-line tool written in Python to detect basic SQL injection vulnerabilities in web applications. It was built as an educational project to demonstrate the fundamentals of web crawling and vulnerability scanning.

> **Disclaimer:** This tool is for educational purposes only. Do not use it on any website or application that you do not own or have explicit, written permission to test. Unauthorized scanning is illegal.

## Features

- **Web Crawler**: Discovers pages on the target website up to a specified depth.
- **Vector Identification**: Finds HTML forms and URL parameters to test.
- **Error-Based Detection**: Identifies vulnerabilities by looking for common SQL error messages in server responses.

## Installation

1. Clone this repository or download all the `.py` files into a single directory.
2. Install the required Python libraries using pip:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the scanner from your terminal. You must provide a starting URL.

```bash
python sqli_sentinel.py --url <target-url> [--depth <number>]
```

## Examples

- **Scan a single page:**

    ```bash
    python sqli_sentinel.py --url http://testphp.vulnweb.com/login.php --depth 0
    ```

- **Crawl and scan a website up to a depth of 2:**

    ```bash
    python sqli_sentinel.py --url http://testphp.vulnweb.com --depth 2
    ```
