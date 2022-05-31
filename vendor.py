"""
Vendor Class
"""
# pylint: disable=logging-fstring-interpolation
#   see: https://github.com/PyCQA/pylint/issues/3512

import logging
import json
from dataclasses import dataclass

import boto3
from botocore.exceptions import ClientError

@dataclass
class Vendor:
    """
    Vendor class
    """
    def __init__(self, domain: str, logger: logging.Logger):
        self.domain = domain
        self.logger = logger
        self.client = boto3.client('dynamodb')
        try:
            result = self.client.get_item(
                TableName="vendors",
                Key={
                    "domain": {
                        "S": self.domain
                    }
                }
            )
            if len(result["Item"]) == 4:
                self.friendly_name = result["Item"]["friendly_name"]["S"]
                self.region = result["Item"]["region"]["S"]
                self.platform = int(result["Item"]["platform"]["N"])# what the fuck
            else:
                self.logger.exception(f"Unexpected results retreiving this vendor: {self.domain}")
                self.logger.exception(f"Output: {json.dumps(result)}")
        except ClientError as error:
            self.logger.exception(f"Obtaining vendor data failed: {self.domain}")
            raise error
