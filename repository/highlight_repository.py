import abc
import json

class HighlightRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def save_books(self, highlight: str, user: str):
        pass

    @abc.abstractmethod
    def get_random_highlights(self, user, number_of_hightlights: int):
        pass



class LocalRepository(HighlightRepository):

    def save_books(self, highlights, user):
        js = json.dumps(highlights)
        f = open(f"highlights-{user}.json", 'w')
        f.write(js)
        f.close()

    def get_random_highlights(self, user, number_of_hightlights: int):
        pass