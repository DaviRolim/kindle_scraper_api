import abc
import json


class HighlightRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def save_highlights(self, highlight: str, user: str):
        pass

    @abc.abstractmethod
    def get_random_highlights(self, number_of_hightlights: int):
        pass



class LocalRepository(HighlightRepository):

    def save_highlights(self, highlights, user='Davi Holanda'):
        js = json.dumps(highlights)
        f = open("highlights.json", 'w')
        f.write(js)
        f.close()

    def get_random_highlights(self, number_of_hightlights: int):
        pass