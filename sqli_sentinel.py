#
# Module: sqli_sentinel.py
#
# This is the main controller and entry point for the application.
# It parses command-line arguments, initializes all other modules,
# and orchestrates the entire scanning process.
#

import argparse
import requests
from reporter import Reporter
from scanner import Scanner
from crawler import Crawler

def main():
    """
    The main function that runs the scanner.
    """
    # --- 1. Setup Command-Line Argument Parser ---
    # We use argparse to create a professional command-line interface.
    parser = argparse.ArgumentParser(description="SQLi Sentinel - A simple SQL injection scanner.")
    parser.add_argument("-u", "--url", dest="url", required=True, help="The starting URL to scan.")
    parser.add_argument("--depth", dest="depth", type=int, default=1, help="The crawl depth (default: 1).")
    
    args = parser.parse_args()
    start_url = args.url
    max_depth = args.depth

    # --- 2. Initialize Modules ---
    reporter = Reporter()
    reporter.print_status("SQLi Sentinel starting...")
    reporter.print_status(f"Target: {start_url} | Crawl Depth: {max_depth}")

    # We use a requests.Session object to persist cookies across requests,
    # which is important for websites that use sessions.
    session = requests.Session()
    # Set a user-agent to mimic a real browser. Some websites block default Python requests.
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'})

    crawler = Crawler(session, reporter)
    scanner = Scanner(session, reporter)

    # --- 3. Start the Crawl ---
    # The crawler discovers all forms and URLs with parameters to test.
    try:
        forms, urls_with_params = crawler.crawl(start_url, max_depth)
    except Exception as e:
        reporter.print_status(f"A critical error occurred during crawling: {e}")
        return

    # --- 4. Scan the Discovered Vectors ---
    reporter.print_status("\nCrawl complete. Starting scan phase...")

    # Scan all discovered forms
    if not forms:
        reporter.print_info("No forms found to test.")
    else:
        reporter.print_info(f"Testing {len(forms)} form(s) for Error-Based SQLi...")
        for form in forms:
            scanner.scan_form_for_error_based_sqli(form)

    # Scan all discovered URLs with parameters
    if not urls_with_params:
        reporter.print_info("No URLs with parameters found to test.")
    else:
        reporter.print_info(f"Testing {len(urls_with_params)} URL(s) for Error-Based SQLi...")
        for url in urls_with_params:
            scanner.scan_url_for_error_based_sqli(url)
            
    # --- 5. Print Final Report ---
    reporter.print_summary()


# This is the standard Python entry point.
if __name__ == "__main__":
    main()
