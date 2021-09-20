from datetime import datetime

from celery import shared_task
from data_scraping.http.requests_client import RequestsHttpClient
from data_scraping.html.web_gatherer import HtmlWebGatherer
from data_scraping.scrapers.picker import ScraperPicker

from apps.dashboard.models import Currency, Offer, Phone, Shop
from apps.data_collecting.input_scrap_data_prepare import (
    serialize_input_data, 
    deserialize_input_data, 
    generate_input_scrap_data_from_db
)


@shared_task
def worker():
    for data in generate_input_scrap_data_from_db():
        serialized_data = serialize_input_data(data)
        downloader.delay(serialized_data)


@shared_task
def downloader(input_data: dict):
    data = deserialize_input_data(input_data)

    http_client = RequestsHttpClient()
    html_gatherer = HtmlWebGatherer(http_client=http_client)
    html = html_gatherer.get_html(url=data.offer_url)  

    scraper.delay(html, input_data)
    return html


@shared_task
def scraper(html: str, input_data: dict):
    data = deserialize_input_data(input_data)

    picked_scraper = ScraperPicker(data.offer_url).pick()
    scraper = picked_scraper(offer_page_html=html)
    price = scraper.get_price()

    input_data = deserialize_input_data(input_data)
    phone = Phone.objects.get(id=input_data.phone_id)
    shop = Shop.objects.get(id=input_data.shop_id)
    currency = Currency.objects.get(code="PLN")
    offer = Offer(
        date=datetime.now(),
        price=price,
        currency=currency,
        phone=phone,
        shop=shop,
        url=input_data.offer_url
    )
    offer.save()
    return price