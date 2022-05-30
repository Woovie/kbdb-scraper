"""
The file which AWS Lambda will execute
"""

import vendor

def lambda_handler(event, _):
    """
    a
    """
    # pylint: disable=C0415
    # Lambda is CPU and memory constrained, we only want to import when absolutely necessary
    domain = event["domain"]
    vendor_helper = vendor.Vendor(domain)
    if vendor_helper.platform == "shopfiy":# TODO replace with match case in 3.10
        import shopify
        scraper = shopify.Shopify(domain)
        results = scraper.compile()
        print(results)
