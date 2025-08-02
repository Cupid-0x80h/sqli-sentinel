#
# Module: reporter.py
#
# This module is responsible for all console output.
# It helps in formatting messages and printing them with colors
# to distinguish between status updates, info, and critical vulnerability alerts.
#

# We define ANSI escape codes for colors to make the output more readable.
class Colors:
    """A class to hold ANSI color codes for terminal output."""
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m' # Resets the color

class Reporter:
    """Handles all printing to the console for the application."""

    def __init__(self):
        """
        Initializes the Reporter.
        It also keeps a list of all vulnerabilities found during the scan.
        """
        self.vulnerabilities = []

    def print_status(self, message):
        """Prints a general status message (e.g., "Crawling URL...")."""
        print(f"{Colors.BLUE}[*] {message}{Colors.ENDC}")

    def print_info(self, message):
        """Prints an informational message (e.g., "Found a form.")." """
        print(f"{Colors.GREEN}[+] {message}{Colors.ENDC}")

    def report_vulnerability(self, vulnerability_details):
        """
        Prints a critical vulnerability alert and stores it for the final summary.
        
        Args:
            vulnerability_details (dict): A dictionary containing info about the vulnerability.
        """
        message = (
            f"SQLi Vulnerability Found!\n"
            f"  - URL: {vulnerability_details['url']}\n"
            f"  - Parameter: {vulnerability_details['parameter']}\n"
            f"  - Type: {vulnerability_details['type']}"
        )
        print(f"\n{Colors.RED}[!] {message}{Colors.ENDC}\n")
        self.vulnerabilities.append(vulnerability_details)

    def print_summary(self):
        """Prints a summary of all found vulnerabilities at the end of the scan."""
        self.print_status("Scan Complete.")
        if not self.vulnerabilities:
            self.print_info("No SQL injection vulnerabilities were found.")
        else:
            self.print_info(f"Found {len(self.vulnerabilities)} vulnerabilities:")
            for vuln in self.vulnerabilities:
                print(f"  - URL: {vuln['url']}, Parameter: {vuln['parameter']}, Type: {vuln['type']}")

