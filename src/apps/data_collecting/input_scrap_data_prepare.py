from dataclasses import dataclass

from .models import OffersScrapingData

@dataclass
class InputScrapData:
    phone_id: int
    shop_id: int
    offer_url: str


def serialize_input_data(input_data: InputScrapData):
    return {
        "phone_id": input_data.phone_id,
        "shop_id": input_data.shop_id,
        "offer_url": input_data.offer_url
    }


def deserialize_input_data(input_data: dict):
    return InputScrapData(
        phone_id=input_data["phone_id"],
        shop_id=input_data["shop_id"],
        offer_url=input_data["offer_url"]
    )


def generate_input_scrap_data_from_db():
    objects_generator = OffersScrapingData.objects.all().iterator(chunk_size=100)
    for obj in objects_generator:
        yield InputScrapData(
            phone_id=obj.phone.id,
            shop_id=obj.shop.id,
            offer_url=obj.url
        ) 
