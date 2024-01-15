import time
from enum import Enum

import yagooglesearch
from googletrans import Translator

from foxycon.exception_foxy_con import ExceptionLanguageFormat, \
    ExceptionCountryFormat
from foxycon.utils.AutoSessionRecipient import AutomaticSessionRecipient
from foxycon.utils.AutoManagementProxy import AutoManagementProxy

search = yagooglesearch.SearchClient


class DataGoogleSearch:
    def __init__(self, language, country, period, num = 100, proxy = None, type_search = 'standard'):
        self.language = language
        self.country = country
        self._google_cookies = AutomaticSessionRecipient().get_google()
        self._proxy = self.get_proxy(proxy)
        self._period = period
        self._num = num
        self._type_search = self.get_status_settings(type_search)

    @property
    def country(self):
        return self._country

    @country.setter
    def country(self, con):
        try:
            Country(con)
            self._country = con
        except Exception as ex:
            raise ExceptionCountryFormat(f'The search country is incorrect: {ex}')

    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, lang):
        try:
            Language(lang)
            self._language = lang
        except Exception as ex:
            raise ExceptionLanguageFormat(f'The search language is incorrect: {ex}')

    @staticmethod
    def get_proxy(data_proxy):
        if data_proxy != None:
            return AutoManagementProxy(data_proxy)
        else:
            return ""

    def get_status_settings(self, type_search):
        if TypeSearch[type_search].value == 2:
            translator = Translator()
            data = translator.translate(self._text, dest = str(self._language).split('lang_')[1])
            self._text = data.text

    @staticmethod
    def get_data(text, country, language, period, num, cookies, proxy):
        url = []
        links = search(f'{text}', tbs = Time[period].value, country = country,
                       http_429_cool_off_time_in_minutes = 15,
                       http_429_cool_off_factor = 1.5,
                       google_exemption = cookies,
                       lang_result = language,
                       verbosity = 4,
                       proxy = proxy,
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

    def get_google_dork(self, text):
        return self.get_data(text = f'{text}', country = self._country, language = self._language,
                             period = self._period, cookies = self._google_cookies, num = self._num,
                             proxy = self._proxy)

    def get_facebook(self, text):
        return self.get_data(text = f'site:facebook.com {text}', country = self._country,
                             language = self._language, period = self._period, cookies = self._google_cookies,
                             num = self._num, proxy = self._proxy)

    def get_twitter(self, text):
        return self.get_data(text = f'site:twitter.com {text}', country = self._country,
                             language = self._language, period = self._period, num = self._num, proxy = self._proxy)

    def get_vk(self, text):
        return self.get_data(text = f'site:vk.com {text}', country = self._country, language = self._language,
                             period = self._period, cookies = self._google_cookies, num = self._num,
                             proxy = self._proxy)

    def get_discord(self, text):
        return self.get_data(text = f'site:vk.com {text}', country = self._country, language = self._language,
                             period = self._period, cookies = self._google_cookies, num = self._num,
                             proxy = self._proxy)

    def get_discord(self, text):
        return self.get_data(text = f'site:discord.com {text}', country = self._country,
                             language = self._language, period = self._period, cookies = self._google_cookies,
                             num = self._num, proxy = self._proxy)

    def get_instagram(self, text):
        return self.get_data(text = f'site:www.instagram.com {text}', country = self._country,
                             language = self._language, period = self._period, cookies = self._google_cookies,
                             num = self._num, proxy = self._proxy)

    def get_instagram_hashtag(self, text):
        return self.get_data(text = f'site:www.instagram.com #{text}', country = self._country,
                             language = self._language, period = self._period, cookies = self._google_cookies,
                             num = self._num, proxy = self._proxy)

    def get_instagram_reels(self, text):
        return self.get_data(text = f'site:https://www.instagram.com inurl:reels #{text}', country = self._country,
                             language = self._language, period = self._period, cookies = self._google_cookies,
                             num = self._num, proxy = self._proxy)

    def get_youtube(self, text):
        return self.get_data(text = f'site:youtube.com {text}', country = self._country,
                             language = self._language, period = self._period, cookies = self._google_cookies,
                             num = self._num, proxy = self._proxy)


class Country(Enum):
    usa = 'us'
    india = 'in'
    brazil = 'br'
    canada = 'ca'


class Language(Enum):
    english = 'lang_en'
    portuguese = 'lang_pt'
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
