from pathlib import Path
from data_scraping.scrapers.exceptions import PhoneUnavailable

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


def test_get_price_raises(test_html):
    with pytest.raises(PhoneUnavailable):
        KomputronikScraper(offer_page_html=test_html).get_price()


def test_get_price_success(mocker, test_html):
    mocked_js_event_dict = {
        "ecommerce": {
            "currencyCode": "PLN",
            "detail": {
                "products": [
                    {
                        "price": "4199",
                        "availability": "available"
                    }
                ]
            }
        }
    }
    mocker.patch(
        "data_scraping.scrapers.komputronik.KomputronikScraper.extract_ecommerce_js_event_dict", 
        return_value=mocked_js_event_dict
    )

    scraper = KomputronikScraper(offer_page_html=test_html)
    assert scraper.get_price() == Decimal(4199)

def test_is_phone_available_true():
    test_event_dict = {
        "ecommerce": {
            "detail": {
                "products": [
                    {
                        "availability": "available"
                    }
                ]
            }
        }
    }

    assert KomputronikScraper.is_phone_available(test_event_dict) is True


def test_is_phone_available_false():
    test_event_dict = {
        "ecommerce": {
            "detail": {
                "products": [
                    {
                        "availability": "unavailable"
                    }
                ]
            }
        }
    }

    assert KomputronikScraper.is_phone_available(test_event_dict) is False


def test_is_phone_available_raises():
    test_event_dict = {
        "ecommerce": {
            "detail": {
                "products": [
                    {
                        "availability": "unexpected_status"
                    }
                ]
            }
        }
    }

    with pytest.raises(NotImplementedError):
        KomputronikScraper.is_phone_available(test_event_dict)