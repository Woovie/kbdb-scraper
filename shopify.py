"""
Shopify Scraper class
"""
# pylint: disable=logging-fstring-interpolation
#   see: https://github.com/PyCQA/pylint/issues/3512

import requests
import stocks
from scraper import Scrape

transforms = {
    "url": "$VENDOR_URL/products/{}.handle",
    "stock": "$BOOL_AVG({}.variants.{each}.available)",
    "price": "$MIN_MAX({}.variants.{each}.price)",
    "name": "{}.title",
    "quantity": False,
    "category": "{}.product_type"
}

class Shopify(Scrape):
    """
    Shopify variant of the Scrape class
    """
    def scrape(self) -> bool:
        """
        Does a simple requests call to get products.json data for a vendor
        """
        products = []
        more_products = True
        counter = 1
        while more_products:
            result = requests.get(f"https://{self.domain}/products.json?limit=250&page={counter}")
            json_response = result.json()
            products.extend(json_response["products"])
            if len(json_response["products"]) < 250:
                more_products = False
            counter += 1

        self.results = products
        return True

    def url_transform(self, product: dict) -> str:
        """
        a
        """
        return f"{self.domain}/products/{product['handle']}"

    @staticmethod
    def stock_transform(product: dict) -> str:
        """
        Stuff happens

        Truth table:
        +----------+----------+--------+
        | all_true | any_true | stock? |
        +----------+----------+--------+
        | True     | False    | N/a    | This specific scenario is impossible given all()
        | False    | False    | No     |
        | True     | True     | Yes    |
        | False    | True     | Some   |
        +----------+----------+--------+
        """
        variants_stock = list(map(lambda n: n["available"], product["variants"]))
        all_true = all(variants_stock)
        any_true = any(variants_stock)
        result = None
        if all_true and any_true:
            result = stocks.Stock.LIMITED.value
        elif all_true and not any_true:
            result = stocks.Stock.YES.value
        else:
            result = stocks.Stock.NO.value
        return result

    @staticmethod
    def price_transform(product: dict) -> list:
        """
        Returns a tuple of the min and max price of the variant
        """
        variants_price = list(map(lambda n: n["price"], product["variants"]))
        return {"min": min(variants_price), "max": max(variants_price)}

    @staticmethod
    def name_transform(product: dict) -> str:
        """
        Returns the product's name
        """
        return product["title"]

    @staticmethod
    def category_transform(product: dict) -> str:
        """
        Returns the "product type" as defined by the vendor

        TODO This method likely needs vendor-specific settings
        """
        return product["product_type"]

    def transform_products(self) -> bool:
        """
        Transforms each product
        """
        for product in self.results:
            new_product = {}
            new_product["url"] = self.url_transform(product)
            new_product["stock"] = self.stock_transform(product)
            new_product["price"] = self.price_transform(product)
            new_product["name"] = self.name_transform(product)
            # TODO quantity
            new_product["category"] = self.category_transform(product)
            self.products.append(new_product)
        return True

    def compile(self):
        """
        a
        """
        self.scrape()
        self.transform_products()
        return self.products
