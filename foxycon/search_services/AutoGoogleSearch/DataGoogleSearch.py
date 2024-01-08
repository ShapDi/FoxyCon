import time
from enum import Enum

import yagooglesearch
from googletrans import Translator

from foxycon.utils.AutoSessionRecipient import AutomaticSessionRecipient


search = yagooglesearch.SearchClient

class DataGoogleSearch:
    def __init__(self, language, country, period, num = 100, text = 'search', type_search = 'standard'):
        self._text = text
        self._language = language
        self._country = country
        self._period = period
        self._num = num
        self._type_search = self.get_status_settings(type_search)

    def get_status_settings(self, type_search):
        if TypeSearch[type_search].value == 2:
            translator = Translator()
            data = translator.translate(self._text, dest = str(self._language).split('lang_')[1])
            self._text = data.text

    @staticmethod
    def get_data(text, country, language, period, num):
        url = []
        links = search(f'{text}', tbs = Time[period].value, country = country,
                       http_429_cool_off_time_in_minutes = 15,
                       http_429_cool_off_factor = 1.5,
                       google_exemption = AutomaticSessionRecipient().get_google(),
                       lang_result = language,
                       verbosity = 4,
                       verify_ssl = False,
                       num = num
                       )
        links.verify_ssl = False
        links.assign_random_user_agent()

        time.sleep(60)
        links = links.search()

        if "HTTP_429_DETECTED" in links:
            print("HTTP 429 detected...it's up to you to modify your search.")
            links.remove("HTTP_429_DETECTED")
            print("URLs found before HTTP 429 detected...")
            for link in links:
                url.append(link)
        for link in links:
            url.append(link)
        return url

    def get_google_dork(self):
        return self.get_data(text = f'{self._text}', country = self._country, language = self._language,
                             period = self._period, num = self._num)

    def get_facebook(self):
        return self.get_data(text = f'site:facebook.com {self._text}', country = self._country,
                             language = self._language, period = self._period, num = self._num)

    def get_twitter(self):
        return self.get_data(text = f'site:twitter.com {self._text}', country = self._country,
                             language = self._language, period = self._period, num = self._num)

    def get_vk(self):
        return self.get_data(text = f'site:vk.com {self._text}', country = self._country, language = self._language,
                             period = self._period, num = self._num)

    def get_discord(self):
        return self.get_data(text = f'site:vk.com {self._text}', country = self._country, language = self._language,
                             period = self._period, num = self._num)

    def get_discord(self):
        return self.get_data(text = f'site:discord.com {self._text}', country = self._country,
                             language = self._language, period = self._period, num = self._num)

    def get_instagram(self):
        return self.get_data(text = f'site:www.instagram.com {self._text}', country = self._country,
                             language = self._language, period = self._period, num = self._num)

    def get_instagram_hashtag(self):
        return self.get_data(text = f'site:www.instagram.com #{self._text}', country = self._country,
                             language = self._language, period = self._period, num = self._num)

    def get_instagram_reels(self):
        return self.get_data(text = f'site:https://www.instagram.com inurl:reels #{self._text}', country = self._country,
                             language = self._language, period = self._period, num = self._num)

    def get_youtube(self):
        return self.get_data(text = f'site:youtube.com {self._text}', country = self._country,
                             language = self._language, period = self._period, num = self._num)


class Country(Enum):
    usa = 'us'
    india = 'in'
    brazil = 'br'
    canada = 'ca'

class Language(Enum):
    english = 'lang_en'
    portuguese = 'pt'
    hindi = 'lang_hi'

class Time(Enum):
    year = 'qdr:y'
    month = 'qdr:m'
    week = 'qdr:w'
    day = 'qdr:d'
    hour = 'qdr:h'


class TypeSearch(Enum):
    standard = 1
    translation = 2
