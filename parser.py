#
# Module: parser.py
#
# This module is responsible for parsing HTML content. It uses BeautifulSoup4
# to extract all links and forms from a given page, which are the primary
# targets for our crawler and scanner.
#

from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

class HTMLParser:
    """
    Parses HTML to extract links and forms.
    """

    def __init__(self, base_url):
        """
        Initializes the Parser.

        Args:
            base_url (str): The base URL of the target website. This is used
                            to resolve relative links (e.g., "/about.html")
                            into absolute links (e.g., "http://example.com/about.html").
        """
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc

    def _is_within_scope(self, url):
        """
        Checks if a given URL is within the same domain as the base URL.
        This prevents the crawler from leaving the target website.
        """
        return urlparse(url).netloc == self.base_domain

    def extract_links(self, page_html):
        """
        Finds all unique, in-scope links from the HTML of a page.

        Args:
            page_html (str): The HTML content of the page.

        Returns:
            set: A set of unique, absolute URLs found on the page.
        """
        soup = BeautifulSoup(page_html, 'html.parser')
        links = set()
        for a_tag in soup.find_all('a', href=True):
            href = a_tag.get('href')
            # urljoin handles all cases: absolute links, relative links, etc.
            absolute_link = urljoin(self.base_url, href)
            
            # We only add the link if it's on the same website.
            if self._is_within_scope(absolute_link):
                links.add(absolute_link)
        return links

    def extract_forms(self, page_html):
        """
        Finds all forms on a page and extracts their details.

        Args:
            page_html (str): The HTML content of the page.

        Returns:
            list: A list of dictionaries, where each dictionary represents a form.
        """
        soup = BeautifulSoup(page_html, 'html.parser')
        forms = []
        for form_tag in soup.find_all('form'):
            action = form_tag.get('action')
            method = form_tag.get('method', 'get') # Default to GET if not specified

            # Resolve the form's action URL to be absolute
            target_url = urljoin(self.base_url, action)

            inputs = []
            for input_tag in form_tag.find_all(['input', 'textarea', 'select']):
                input_name = input_tag.get('name')
                input_type = input_tag.get('type', 'text')
                # We need the name to submit the form data
                if input_name:
                    inputs.append({'name': input_name, 'type': input_type})
            
            forms.append({
                'action': target_url,
                'method': method,
                'inputs': inputs
            })
        return forms
