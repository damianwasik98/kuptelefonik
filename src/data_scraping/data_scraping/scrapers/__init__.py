from .komputronik import KomputronikScraper
from .rtv_euro_agd import RTVEuroAGDScraper

FLD_SCRAPER_MAP = {
    "komputronik.pl": KomputronikScraper,
    "euro.com.pl": RTVEuroAGDScraper
}