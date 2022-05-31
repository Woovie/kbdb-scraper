"""
TODO
"""

import json
import logging

import stores

def lambda_handler(event, _):
    """
    TODO
    """
    logger=logging.getLogger(__name__)
    logger.setLevel('DEBUG')
    sns_message = json.loads(event["Records"][0]["Sns"]["Message"])
    platform = stores.Platform(sns_message["platform"])
    if hasattr(Platforms, platform.name.lower()):
        getattr(Platforms, platform.name.lower())(sns_message["domain"], logger)

class Platforms:
    """
    TODO
    """

    @staticmethod
    def shopify(domain: str, logger: logging.Logger):
        """
        Shopify-specific actions to take
        """
        # pylint: disable=C0415
        # Lambda is CPU and memory constrained, we only want to import when absolutely necessary
        import shopify
        scraper = shopify.Shopify(domain, logger=logger)
        results = scraper.compile()
