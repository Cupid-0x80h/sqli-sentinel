#
# Module: crawler.py
#
# This module is responsible for navigating the target website. It starts
# at a given URL, finds all links on the page, and adds them to a queue
# to visit. It ensures that it doesn't scan the same page twice and doesn't
# leave the target website.
#

import requests
from parser import HTMLParser

class Crawler:
    """
    A web crawler that discovers pages and attack vectors on a website.
    """

    def __init__(self, session, reporter):
        """
        Initializes the Crawler.

        Args:
            session (requests.Session): The session object for making HTTP requests.
            reporter (Reporter): The reporter object for printing output.
        """
        self.session = session
        self.reporter = reporter
        self.visited_urls = set()

    def crawl(self, start_url, max_depth):
        """
        Starts the crawling process.

        Args:
            start_url (str): The URL to begin crawling from.
            max_depth (int): The maximum depth to crawl. 0 means only scan the start_url.

        Returns:
            tuple: A tuple containing a list of forms found and a set of URLs with parameters.
        """
        # The "frontier" is our to-do list of URLs to crawl.
        # We store it as a list of tuples: (url, current_depth)
        frontier = [(start_url, 0)]
        all_forms = []
        urls_with_params = set()
        
        parser = HTMLParser(start_url)

        while frontier:
            current_url, current_depth = frontier.pop(0)

            if current_url in self.visited_urls or current_depth > max_depth:
                continue

            self.reporter.print_status(f"Crawling [Depth: {current_depth}]: {current_url}")
            self.visited_urls.add(current_url)

            try:
                response = self.session.get(current_url, timeout=10)
                if "text/html" not in response.headers.get("Content-Type", ""):
                    continue # Skip non-HTML pages

                page_html = response.text
                
                # --- Find new links to crawl ---
                new_links = parser.extract_links(page_html)
                for link in new_links:
                    if link not in self.visited_urls:
                        frontier.append((link, current_depth + 1))
                
                # --- Find forms on the current page ---
                forms_on_page = parser.extract_forms(page_html)
                if forms_on_page:
                    self.reporter.print_info(f"Found {len(forms_on_page)} form(s) on {current_url}")
                    all_forms.extend(forms_on_page)

                # --- Check if the URL itself has parameters ---
                if '?' in current_url:
                    urls_with_params.add(current_url)

            except requests.exceptions.RequestException as e:
                self.reporter.print_status(f"Could not crawl {current_url}: {e}")

        return all_forms, urls_with_params
