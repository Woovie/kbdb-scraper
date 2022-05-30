"""
Vendor Class
"""
# pylint: disable=logging-fstring-interpolation
#   see: https://github.com/PyCQA/pylint/issues/3512

import logging
from dataclasses import dataclass

import boto3
from botocore.exceptions import ClientError

@dataclass
class Vendor:
    """
    Vendor class
    """
    def __init__(self, domain: str, logger: str = __name__):
        self.domain = domain
        self.logger = logging.getLogger(logger)
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
            if len(result["Item"]) == 1:
                self.friendly_name = result["Item"]["friendly_name"]["S"]
                self.region = result["Item"]["region"]["S"]
                self.platform =  result["Item"]["platform"]["S"]
            else:
                raise ClientError
        except ClientError as error:
            self.logger.exception(f"Obtaining vendor data failed: {self.domain}")
            raise error
