from pathlib import Path
from data_scraping.scrapers.exceptions import PhoneUnavailable, PriceNotFoundOnPage

import pytest
from decimal import Decimal

from data_scraping.scrapers.rtv_euro_agd import RTVEuroAGDScraper
from data_scraping.html.file_gatherer import HtmlFileGatherer


@pytest.fixture
def test_html():
    test_file_path = Path(__file__).parent / Path("fixtures/rtv_euro_agd.html")
    test_html = HtmlFileGatherer().get_html(test_file_path)
    return test_html


def test_parse_js_dict():
    js_raw_dict = """
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

    assert RTVEuroAGDScraper._parse_js_dict(js_raw_dict) == expected_python_dict


def test_extract_price_from_product_dict():
    product_dict = {
        "price": "4449.00"
    }
    price = RTVEuroAGDScraper.extract_price_from_product_dict(product_dict)
    assert isinstance(price, Decimal)
    assert price == Decimal(4449.00)


def test_extract_product_dict_from_html(test_html):
    assert RTVEuroAGDScraper(offer_page_html=test_html).extract_product_dict_from_html() == {
		"id": 72565423201,
		"title": "Apple iPhone 12‌ 128GB (czarny)",
		"plu": "1225739",
		"groupId": 698969,
		"groupName": "Smartfony i telefony",
		"brand": "Apple",
		"price": "4449.00",
		"category": "Smartfony i gadżety",
		"supplierId": "",
		"photo": "/foto/9/72565423201/c9cb977a131b39ace5e4cf83c97abc05/apple-iphone-12-czarny,72565423201_2.jpg",
		"productAvailabilityStatusCode": "6",
		"unavailableAtTheMoment": False,
		"productCardTestEnabled": True,
		"navItems": [
			{"name": "Akcesoria", "hash": "akcesoria"}, 
			{"name": "Opis produktu", "hash": "opis"}, 
			{"name": "Dane techniczne", "hash": "specyfikacja"}, 
			{"name": "Opinie (24)", "hash": "opinie"}, 
			{"name": "Pytania i odpowiedzi (5)", "hash": "pytania"}, 
		],
		"successorProductId": "",
		"showProductVariantPriceDifferences": True,
		"linkName": "apple-iphone-12-czarny",
		"nodeId": "telefony-komorkowe",
		"preview": False,
		"showDescriptionGrade": False,
		"productActive": True,
		"productPromotionAvailable": False,
		"outletPromotionAvailable": False,
		"warrantyChangeConflictMessage": {
			"header": 'Zmiana wariantu Ochrony spowoduje rezygnację z wybranej oferty ratalnej.',
			"content": 'Czy chcesz zrezygnować z Rat z Ochroną sprzętu?'
		},
		"configurationDto": {
			"defaultSelectedOutletCategoryId": "",
			"defaultInstalmentOption": {
				"available": False,
				"code": "",
				"number": "0",
				"paymentType": "",
				"instalmentWarrantyId": ""
			},
			"availableOutletCategories": [],
		}
	}


def test_get_price_phone_available(test_html):
    assert RTVEuroAGDScraper(offer_page_html=test_html).get_price() == Decimal(4449.00)


def test_get_price_phone_unavailable(mocker):
    mocked_product_dict = {
        "unavailableAtTheMoment": True,
    }
    mocker.patch("data_scraping.scrapers.rtv_euro_agd.RTVEuroAGDScraper.extract_product_dict_from_html", return_value=mocked_product_dict)
    with pytest.raises(PhoneUnavailable):
        assert RTVEuroAGDScraper(offer_page_html=test_html).get_price() == Decimal(4449.00)


def test_is_phone_available():
    test_dict = {
        "unavailableAtTheMoment": True
    }

    assert RTVEuroAGDScraper.is_phone_available(product_dict=test_dict) is False
