
class PriceNotFoundOnPage(Exception):
    
    def __init__(self, page_html):
        self.page_html = page_html
        super().__init__("Price was not found on page. Check price parser logic.")


class InvalidURL(Exception):

    def __init__(self, url):
        self.url = url
        super().__init__(url)

    def __str__(self):
        return f"{self.url} is not valid URL"

    
class PhoneUnavailable(Exception):

    def __init__(self, page_html):
        self.page_html =  page_html
        super().__init__("Phone is unavailable at the moment.")