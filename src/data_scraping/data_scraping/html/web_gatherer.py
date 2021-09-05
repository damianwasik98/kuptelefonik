from pathlib import Path

from data_scraping.html.base_gatherer import HtmlGatherer
from data_scraping.http.base_client import HttpClient

class HtmlWebGatherer(HtmlGatherer):
    
    def __init__(self, http_client: HttpClient) -> None:
        self.http_client = http_client

    def get_html(self, url: str) -> str:
        TIMEOUT = 60
        response = self.http_client.get(url=url, timeout=TIMEOUT)
        html = response.text
        return html

    def save_html(self, html, file_path: str) -> None:
        path = Path(file_path)
        with open(path, "w") as file:
            file.write(html)