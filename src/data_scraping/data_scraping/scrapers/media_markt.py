from decimal import Decimal
import logging

from data_scraping.scrapers.base_scraper import PhoneOfferScraper
from data_scraping.scrapers.exceptions import PriceNotFoundOnPage

logger =  logging.getLogger(__name__)


class MediaMarktScraper(PhoneOfferScraper):

    def __init__(self, offer_page_html: str) -> None:
        self.offer_page_html = offer_page_html

    def get_price(self) -> Decimal:
        pass
