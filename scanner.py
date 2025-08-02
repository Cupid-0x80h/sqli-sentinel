#
# Module: scanner.py
#
# This is the core engine of the tool. It receives potential attack vectors
# (like forms or URLs with parameters) and tests them for SQL injection vulnerabilities.
#

import requests
from urllib.parse import urljoin

class Scanner:
    """
    The main scanning engine that tests for various types of SQL injection.
    """

    def __init__(self, session, reporter):
        """
        Initializes the Scanner.

        Args:
            session (requests.Session): The session object to maintain cookies and headers.
            reporter (Reporter): The reporter object for printing output.
        """
        self.session = session
        self.reporter = reporter

        # A list of common SQL error messages across different database systems.
        # Our error-based scanner will look for these strings in the response page.
        self.sql_error_messages = [
            "you have an error in your sql syntax;",
            "warning: mysql",
            "unclosed quotation mark",
            "syntax error",
            "invalid input syntax for type"
        ]
        
        # A simple payload to test for error-based SQLi.
        self.error_based_payload = "'"

    def scan_url_for_error_based_sqli(self, url):
        """
        Tests a given URL for error-based SQLi by injecting a payload
        into its parameters.

        Args:
            url (str): The URL to test, which may or may not have parameters.
        """
        # We append our malicious payload to the end of the URL
        malicious_url = f"{url}{self.error_based_payload}"
        self.reporter.print_status(f"Testing for Error-Based SQLi on URL: {malicious_url}")

        try:
            # Send the request
            response = self.session.get(malicious_url, timeout=10)
            
            # Check the response content for any of our known error messages
            for error in self.sql_error_messages:
                if error in response.text.lower():
                    # VULNERABILITY FOUND!
                    self.reporter.report_vulnerability({
                        'url': url,
                        'parameter': 'URL Parameter',
                        'type': 'Error-Based SQLi'
                    })
                    # Once we find a vulnerability on this URL, we don't need to check further.
                    return True
        except requests.exceptions.RequestException as e:
            self.reporter.print_status(f"An error occurred while testing {malicious_url}: {e}")
        
        return False


    def scan_form_for_error_based_sqli(self, form_details):
        """
        Tests a given HTML form for error-based SQLi.

        Args:
            form_details (dict): A dictionary containing the form's action, method, and inputs.
        """
        target_url = form_details["action"]
        method = form_details["method"].lower()
        inputs = form_details["inputs"]

        # This dictionary will hold the data we submit with the form
        data_payload = {}
        
        # We test each input field one by one
        for input_field in inputs:
            input_name = input_field.get("name")
            input_type = input_field.get("type", "text") # Default to text if no type

            # We don't want to inject into buttons or hidden fields usually
            if input_type in ["submit", "button", "hidden"]:
                continue

            # Populate the data payload with default values for all fields
            for i in inputs:
                if i.get("name"):
                    data_payload[i.get("name")] = "test"
            
            # Now, overwrite the field we are currently testing with our malicious payload
            data_payload[input_name] = self.error_based_payload

            self.reporter.print_status(f"Testing form on {target_url} with payload in '{input_name}' field")

            try:
                # Submit the form (either as a GET or POST request)
                if method == "post":
                    response = self.session.post(target_url, data=data_payload, timeout=10)
                else: # Assumes GET if not POST
                    response = self.session.get(target_url, params=data_payload, timeout=10)

                # Check the response for error messages, just like with the URL scan
                for error in self.sql_error_messages:
                    if error in response.text.lower():
                        # VULNERABILITY FOUND!
                        self.reporter.report_vulnerability({
                            'url': target_url,
                            'parameter': input_name,
                            'type': 'Error-Based SQLi (Form)'
                        })
                        # We found a vulnerability in this form, so we can stop testing it.
                        return True

            except requests.exceptions.RequestException as e:
                self.reporter.print_status(f"An error occurred while testing form on {target_url}: {e}")
        
        return False

#
# Module: scanner.py
#
# This is the core engine of the tool. It receives potential attack vectors
# (like forms or URLs with parameters) and tests them for SQL injection vulnerabilities.
#

import requests
from urllib.parse import urljoin

class Scanner:
    """
    The main scanning engine that tests for various types of SQL injection.
    """

    def __init__(self, session, reporter):
        """
        Initializes the Scanner.

        Args:
            session (requests.Session): The session object to maintain cookies and headers.
            reporter (Reporter): The reporter object for printing output.
        """
        self.session = session
        self.reporter = reporter

        # A list of common SQL error messages across different database systems.
        # Our error-based scanner will look for these strings in the response page.
        self.sql_error_messages = [
            "you have an error in your sql syntax;",
            "warning: mysql",
            "unclosed quotation mark",
            "syntax error",
            "invalid input syntax for type"
        ]
        
        # A simple payload to test for error-based SQLi.
        self.error_based_payload = "'"

    def scan_url_for_error_based_sqli(self, url):
        """
        Tests a given URL for error-based SQLi by injecting a payload
        into its parameters.

        Args:
            url (str): The URL to test, which may or may not have parameters.
        """
        # We append our malicious payload to the end of the URL
        malicious_url = f"{url}{self.error_based_payload}"
        self.reporter.print_status(f"Testing for Error-Based SQLi on URL: {malicious_url}")

        try:
            # Send the request
            response = self.session.get(malicious_url, timeout=10)
            
            # Check the response content for any of our known error messages
            for error in self.sql_error_messages:
                if error in response.text.lower():
                    # VULNERABILITY FOUND!
                    self.reporter.report_vulnerability({
                        'url': url,
                        'parameter': 'URL Parameter',
                        'type': 'Error-Based SQLi'
                    })
                    # Once we find a vulnerability on this URL, we don't need to check further.
                    return True
        except requests.exceptions.RequestException as e:
            self.reporter.print_status(f"An error occurred while testing {malicious_url}: {e}")
        
        return False


    def scan_form_for_error_based_sqli(self, form_details):
        """
        Tests a given HTML form for error-based SQLi.

        Args:
            form_details (dict): A dictionary containing the form's action, method, and inputs.
        """
        target_url = form_details["action"]
        method = form_details["method"].lower()
        inputs = form_details["inputs"]

        # This dictionary will hold the data we submit with the form
        data_payload = {}
        
        # We test each input field one by one
        for input_field in inputs:
            input_name = input_field.get("name")
            input_type = input_field.get("type", "text") # Default to text if no type

            # We don't want to inject into buttons or hidden fields usually
            if input_type in ["submit", "button", "hidden"]:
                continue

            # Populate the data payload with default values for all fields
            for i in inputs:
                if i.get("name"):
                    data_payload[i.get("name")] = "test"
            
            # Now, overwrite the field we are currently testing with our malicious payload
            data_payload[input_name] = self.error_based_payload

            self.reporter.print_status(f"Testing form on {target_url} with payload in '{input_name}' field")

            try:
                # Submit the form (either as a GET or POST request)
                if method == "post":
                    response = self.session.post(target_url, data=data_payload, timeout=10)
                else: # Assumes GET if not POST
                    response = self.session.get(target_url, params=data_payload, timeout=10)

                # Check the response for error messages, just like with the URL scan
                for error in self.sql_error_messages:
                    if error in response.text.lower():
                        # VULNERABILITY FOUND!
                        self.reporter.report_vulnerability({
                            'url': target_url,
                            'parameter': input_name,
                            'type': 'Error-Based SQLi (Form)'
                        })
                        # We found a vulnerability in this form, so we can stop testing it.
                        return True

            except requests.exceptions.RequestException as e:
                self.reporter.print_status(f"An error occurred while testing form on {target_url}: {e}")
        
        return False

