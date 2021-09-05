from validators import url as is_valid_url
from tld import get_fld

from data_scraping.scrapers.base_scraper import PhoneOfferScraper
from data_scraping.scrapers import FLD_SCRAPER_MAP
from data_scraping.scrapers.exceptions import InvalidURL


class ScraperPicker:

    def __init__(self, url: str):
        self.url = url
    
    def _validate_offer_site_url(self):
        if not is_valid_url:
            raise InvalidURL(self.url)

    def pick(self) -> PhoneOfferScraper:
        self._validate_offer_site_url()

        fld = get_fld(self.url)
        picked_scraper = FLD_SCRAPER_MAP.get(fld)
        if not picked_scraper:
            raise NotImplementedError()
        return picked_scraper