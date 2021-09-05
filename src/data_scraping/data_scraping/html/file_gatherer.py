from data_scraping.html.base_gatherer import HtmlGatherer

class HtmlFileGatherer(HtmlGatherer):

    def get_html(self, file_path: str) -> str:
        with open(file_path, "r") as file:
            return file.read()