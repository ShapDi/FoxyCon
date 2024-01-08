import feedparser
from googletrans import Translator


translator = Translator()

class DataNews:
    def __init__(self, link):
        self._link = link

    def get_data(self):
        NewsFeed = feedparser.parse(f"{self._link}")
        entry = NewsFeed.entries
        list_news = []
        for new in entry:
            list_news.append({'title':new.title, 'translated_title':translator.translate(new.title,dest='ru').text, 'link':new.link})
        return list_news

