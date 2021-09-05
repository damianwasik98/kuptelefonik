import requests
import random

from data_scraping.http.base_client import HttpClient, Response

class RequestsHttpClient(HttpClient):
    TIMEOUT = 60
    USER_AGENTS = [
        ('Mozilla/5.0 (X11; Linux x86_64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/57.0.2987.110 '
        'Safari/537.36'),  # chrome
        ('Mozilla/5.0 (X11; Linux x86_64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/61.0.3163.79 '
        'Safari/537.36'),  # chrome
        ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) '
        'Gecko/20100101 '
        'Firefox/55.0'),  # firefox
        ('Mozilla/5.0 (X11; Linux x86_64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/61.0.3163.91 '
        'Safari/537.36'),  # chrome
        ('Mozilla/5.0 (X11; Linux x86_64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/62.0.3202.89 '
        'Safari/537.36'),  # chrome
        ('Mozilla/5.0 (X11; Linux x86_64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/63.0.3239.108 '
        'Safari/537.36'),  # chrome
    ]

    def _get_user_agent(self):
        picked_user_agent = random.choice(self.USER_AGENTS)
        return "".join(picked_user_agent)

    def get(self, url, timeout: int = TIMEOUT):
        headers = {
            "User-Agent": self._get_user_agent(),
        }
        response = requests.get(url=url, timeout=timeout, headers=headers)
        return Response(
            text=response.text,
            status_code=response.status_code
        )