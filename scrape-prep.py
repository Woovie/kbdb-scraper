"""
a
"""

import json
import logging
import boto3

import vendor
import stores

def lambda_handler(event, _):
    """
    Lambda entrypoint
    """
    # pylint: disable=W1203
    logger = logging.getLogger(__name__)
    logger.setLevel('DEBUG')
    domain = event["domain"]
    vendor_helper = vendor.Vendor(domain, logger=logger)
    platforms = [item.value for item in stores.Platform]
    if vendor_helper.platform in platforms:
        send_to_sns(vendor_helper, logger)
    else:
        logger.exception(f"Unable to find a suitable platform for {domain}.")
        logger.exception(f"  Available platforms: {str(platforms)}")
        logger.exception(f"  Platform provided: {str(vendor_helper.platform)}")

def send_to_sns(vendor_helper: vendor.Vendor, logger: logging.Logger):
    """
    Sends a message to SNS to start scraping process
    """
    sns_message = {
        "domain": vendor_helper.domain,
        "platform": vendor_helper.platform
    }
    sns = boto3.client('sns')
    results = sns.publish(
        TopicArn='arn:aws:sns:us-west-2:150144700298:scraper-vendors',
        Message=json.dumps(sns_message)
    )
    logger.info(f"Pushed {vendor_helper.domain} to SNS, results: {json.dumps(results)}")
