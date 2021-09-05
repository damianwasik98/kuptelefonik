from decimal import Decimal
import logging
import re
from typing import Optional

import demjson

from data_scraping.scrapers.base_scraper import PhoneOfferScraper
from data_scraping.scrapers.exceptions import PriceNotFoundOnPage

logger = logging.getLogger(__name__)


class RTVEuroAGDScraper(PhoneOfferScraper):

    def __init__(self, offer_page_html: str) -> None:
        self.offer_page_html = offer_page_html

    @staticmethod
    def _parse_js_dict(js_dict: str) -> dict:
        return demjson.decode(js_dict)

    @staticmethod
    def extract_price_from_product_dict(product_dict: dict) -> Decimal:
        return Decimal(product_dict["price"])

    def extract_product_dict_from_html(self) -> Optional[dict]:
        product_js_dict_regex = re.compile(r"_PRODUCT=({[^;]+});")
        match = re.search(pattern=product_js_dict_regex, string=self.offer_page_html)
        if not match:
            raise PriceNotFoundOnPage(page_html=self.offer_page_html)
        product_js_dict = match.group(1)
        product_parsed_dict = self._parse_js_dict(product_js_dict)
        return product_parsed_dict

    def get_price(self) -> Decimal:
        product_dict = self.extract_product_dict_from_html()
        return self.extract_price_from_product_dict(product_dict)
