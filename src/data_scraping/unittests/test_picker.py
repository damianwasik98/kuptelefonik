import pytest

from data_scraping.scrapers.picker import ScraperPicker
from data_scraping.scrapers.rtv_euro_agd import RTVEuroAGDScraper

def test_pick_scraper_raises():
    url = "https://www.mediaexpert.pl/smartfony-i-zegarki/smartfony/smartfon-samsung-sm-g991-galaxy-s21-5g-8-128gb-gray"
    picker = ScraperPicker(url)

    with pytest.raises(NotImplementedError):
        picker.pick()


def test_pick_correct_scraper():
    url = "https://www.euro.com.pl/telefony-komorkowe/iphone-12-mini-64gb-czarny.bhtml"

    picked_scraper = ScraperPicker(url).pick()
    assert picked_scraper == RTVEuroAGDScraper
