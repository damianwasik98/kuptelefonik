from abc import ABC, abstractmethod
from decimal import Decimal

class PhoneOfferScraper(ABC):

    @abstractmethod
    def __init__(self, offer_page_html: str) -> None:
        ...

    @abstractmethod
    def get_price(self) -> Decimal:
        ...