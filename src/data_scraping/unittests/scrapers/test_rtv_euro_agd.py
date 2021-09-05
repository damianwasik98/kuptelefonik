from pathlib import Path

import pytest
from decimal import Decimal

from data_scraping.scrapers.rtv_euro_agd import RTVEuroAGDScraper
from data_scraping.html.file_gatherer import HtmlFileGatherer


@pytest.fixture
def product_js_test_dict():
    return """
    {
        id:72565423201,
        title:"Apple iPhone 12‌ 128GB (czarny)",
        plu: "1225739",
        category: "Smartfony i gadżety",
        groupId:698969,
        groupName:"Smartfony i telefony",
        name:"smartfon",
        price : "4449.00",
        link : "/telefony-komorkowe/apple-iphone-12-czarny.bhtml",
        foto : "/foto/9/72565423201/c9cb977a131b39ace5e4cf83c97abc05/apple-iphone-12-czarny,72565423201_2.jpg",
        nodes: [
            {name: "Smartfony i gadżety",id:"145977006"},
            {name: "Telefony i Smartfony",id:"514100664"}]
    }
    """


@pytest.fixture
def test_html():
    test_file_path = Path(__file__).parent / Path("fixtures/rtv_euro_agd.html")
    test_html = HtmlFileGatherer().get_html(test_file_path)
    return test_html


def test_parse_js_dict(product_js_test_dict):
    expected_python_dict = {
        "id": 72565423201,
        "title": "Apple iPhone 12‌ 128GB (czarny)",
        "plu": "1225739",
        "category": "Smartfony i gadżety",
        "groupId": 698969,
        "groupName": "Smartfony i telefony",
        "name": "smartfon",
        "price": "4449.00",
        "link": "/telefony-komorkowe/apple-iphone-12-czarny.bhtml",
        "foto": "/foto/9/72565423201/c9cb977a131b39ace5e4cf83c97abc05/apple-iphone-12-czarny,72565423201_2.jpg",
        "nodes": [
            {"name": "Smartfony i gadżety", "id": "145977006"},
            {"name": "Telefony i Smartfony", "id": "514100664"}]
    }

    assert RTVEuroAGDScraper._parse_js_dict(product_js_test_dict) == expected_python_dict


def test_extract_price_from_product_dict(product_js_test_dict):
    parsed_product_dict = RTVEuroAGDScraper._parse_js_dict(product_js_test_dict)
    price = RTVEuroAGDScraper.extract_price_from_product_dict(parsed_product_dict)
    assert isinstance(price, Decimal)
    assert price == Decimal(4449.00)


def test_extract_product_dict_from_html(test_html):
    assert RTVEuroAGDScraper(offer_page_html=test_html).extract_product_dict_from_html() == {
        "id": 72565423201,
        "title": "Apple iPhone 12‌ 128GB (czarny)",
        "plu": "1225739",
        "category": "Smartfony i gadżety",
        "groupId": 698969,
        "groupName": "Smartfony i telefony",
        "name": "smartfon",
        "price": "4449.00",
        "link": "/telefony-komorkowe/apple-iphone-12-czarny.bhtml",
        "foto": "/foto/9/72565423201/c9cb977a131b39ace5e4cf83c97abc05/apple-iphone-12-czarny,72565423201_2.jpg",
        "nodes": [
            {"name": "Smartfony i gadżety", "id": "145977006"},
            {"name": "Telefony i Smartfony", "id": "514100664"}]
    }


def test_get_price(test_html):
    assert RTVEuroAGDScraper(offer_page_html=test_html).get_price() == Decimal(4449.00)
