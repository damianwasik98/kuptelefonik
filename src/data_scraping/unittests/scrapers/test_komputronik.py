from pathlib import Path

import pytest
from decimal import Decimal

from data_scraping.scrapers.komputronik import KomputronikScraper
from data_scraping.html.file_gatherer import HtmlFileGatherer

@pytest.fixture
def test_js_event_json():
    return """
    {
        "event": "ga.hit",
        "hitType": "pageview",
        "pageCategory": "Produkt",
        "userId": null,
        "userLogged": false,
        "productCategories": [
            "Telefony i Smartwatche",
            "Telefony i Smartfony"
        ],
        "ecommerce": {
            "currencyCode": "PLN",
            "detail": {
                "products": [
                    {
                        "name": "Apple iPhone 12 128GB Czarny",
                        "id": "703593",
                        "price": "4199",
                        "brand": "Apple",
                        "category": "Telefony i Smartfony",
                        "variant": "",
                        "systemCode": "GS-T-APL-0811",
                        "vendorCode": "MGJA3PM/A",
                        "availability": "unavailable"
                    }
                ]
            }
        }
    }    
    """


@pytest.fixture
def test_html():
    test_file_path = Path(__file__).parent / Path("fixtures/komputronik.html")
    test_html = HtmlFileGatherer().get_html(test_file_path)
    return test_html


def test_parse_js_event_json(test_js_event_json):
    assert KomputronikScraper.parse_js_event_json(test_js_event_json) == {
        "event": "ga.hit",
        "hitType": "pageview",
        "pageCategory": "Produkt",
        "userId": None,
        "userLogged": False,
        "productCategories": [
            "Telefony i Smartwatche",
            "Telefony i Smartfony"
        ],
        "ecommerce": {
            "currencyCode": "PLN",
            "detail": {
                "products": [
                    {
                        "name": "Apple iPhone 12 128GB Czarny",
                        "id": "703593",
                        "price": "4199",
                        "brand": "Apple",
                        "category": "Telefony i Smartfony",
                        "variant": "",
                        "systemCode": "GS-T-APL-0811",
                        "vendorCode": "MGJA3PM/A",
                        "availability": "unavailable"
                    }
                ]
            }
        }
    }


def test_extract_price_from_event_dict(test_js_event_json):
    parsed_event_dict = KomputronikScraper.parse_js_event_json(test_js_event_json)
    price = KomputronikScraper.extract_price_from_event_dict(parsed_event_dict)
    assert isinstance(price, Decimal)
    assert price == Decimal(4199)


def test_extract_ecommerce_js_event_dict(test_html):
    assert KomputronikScraper(offer_page_html=test_html).extract_ecommerce_js_event_dict() == {
        "event": "ga.hit",
        "hitType": "pageview",
        "pageCategory": "Produkt",
        "userId": None,
        "userLogged": False,
        "productCategories": [
            "Telefony i Smartwatche",
            "Telefony i Smartfony"
        ],
        "ecommerce": {
            "currencyCode": "PLN",
            "detail": {
                "products": [
                    {
                        "name": "Apple iPhone 12 128GB Czarny",
                        "id": "703593",
                        "price": "4199",
                        "brand": "Apple",
                        "category": "Telefony i Smartfony",
                        "variant": "",
                        "systemCode": "GS-T-APL-0811",
                        "vendorCode": "MGJA3PM/A",
                        "availability": "unavailable"
                    }
                ]
            }
        }
    }


def test_get_price(test_html):
    assert KomputronikScraper(offer_page_html=test_html).get_price() == Decimal(4199)