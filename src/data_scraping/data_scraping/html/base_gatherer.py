from abc import ABC, abstractmethod

class HtmlGatherer(ABC):

    @abstractmethod
    def get_html(self) -> str:
        ...
