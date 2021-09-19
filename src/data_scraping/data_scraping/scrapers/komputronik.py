from decimal import Decimal
from enum import Enum
import json
import logging
import re

from data_scraping.scrapers.base_scraper import PhoneOfferScraper
from data_scraping.scrapers.exceptions import PhoneUnavailable, PriceNotFoundOnPage

logger = logging.getLogger(__name__)


class AvailabilityStatus(Enum):
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"


class KomputronikScraper(PhoneOfferScraper):

    def __init__(self, offer_page_html: str) -> None:
        self.offer_page_html = offer_page_html

    @staticmethod
    def parse_js_event_json(event_json: str) -> dict:
        return json.loads(event_json)

    @staticmethod
    def extract_price_from_event_dict(event_dict: dict) -> Decimal:
        extracted_price = event_dict["ecommerce"]["detail"]["products"][0]["price"]
        return Decimal(extracted_price)

    @staticmethod
    def is_phone_available(event_dict: dict) -> bool:
        status = event_dict["ecommerce"]["detail"]["products"][0]["availability"]
        enum_values = AvailabilityStatus._value2member_map_.keys()

        if status not in enum_values:
            raise NotImplementedError(f"Unknown status {status}")
        
        if status == AvailabilityStatus.AVAILABLE.value:
            return True
        return False


    def extract_ecommerce_js_event_dict(self):
        js_event_json_regex = re.compile(r"dataLayer\.push\(({[^;]+})\);")
        match = re.search(pattern=js_event_json_regex, string=self.offer_page_html)
        if not match:
            raise PriceNotFoundOnPage(page_html=self.offer_page_html)
        js_event_json = match.group(1)
        js_event_dict = self.parse_js_event_json(js_event_json)
        return js_event_dict

    def get_price(self) -> Decimal:
        event_dict = self.extract_ecommerce_js_event_dict()
        if not self.is_phone_available(event_dict):
            raise PhoneUnavailable(page_html=self.offer_page_html)
        return self.extract_price_from_event_dict(event_dict)
