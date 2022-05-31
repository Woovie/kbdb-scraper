"""
KBDB Scraper
"""

import logging
import requests

class Scrape:
    """
    Scraper base class
    """
    def __init__(self, domain: str, logger: logging.Logger):
        self.domain = domain
        self.results = None
        self.products = []
        self.logger = logger

    def scrape(self):
        """
        Basic scrape method, should be overridden for a more platform-specific variant
        """
        result = requests.get(self.domain)
        self.results = result.text

    def compile(self):
        """
        Base compile method, should be overridden for a more platform-specific variant
        """
        return self.results
