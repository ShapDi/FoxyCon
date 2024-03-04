import time
import logging
from enum import Enum

import yagooglesearch
from googletrans import Translator

from foxycon.utils import AutomaticSessionRecipient
from foxycon.search_services.exception import ExceptionLanguageFormat, \
    ExceptionCountryFormat
from foxycon.utils import AutoManagementProxy


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
logger.addHandler(console_handler)


class DataGoogleSearch:

    def __init__(self, language, country, period, num = 100, proxy = None, type_search = 'standard'):
        self._search_manager = None
        self.language = language
        self.country = country
        self.period = period
        self._google_cookies = AutomaticSessionRecipient().get_google()
        self._num = num
        self._type_search = self.get_status_settings(type_search)
        self.get_search_manager(self._language, self._country, self._period, num, proxy, type_search)

    def get_search_manager(self, language, country, period, num, proxy, type_search):
        self._search_manager = []
        if proxy is None:
            self._search_manager.append(yagooglesearch.SearchClient(f'fox', tbs = period, country = country,
                                        google_exemption = AutomaticSessionRecipient().get_google(),
                                        lang_result = language,
                                        verbosity = 4,
                                        verify_ssl = False,
                                        proxy = None,
                                        num = num,
                                        http_429_cool_off_time_in_minutes = 45,
                                        http_429_cool_off_factor = 1.5,
                                        minimum_delay_between_paged_results_in_seconds = 7
                                        ))
            self._search_manager = AutoManagementProxy(self._search_manager)
        else:
            for pro in proxy:
                self._search_manager.append(
                    yagooglesearch.SearchClient(f'fox', tbs = period, country = country,
                                                google_exemption = AutomaticSessionRecipient().get_google(),
                                                lang_result = language,
                                                verbosity = 4,
                                                verify_ssl = False,
                                                proxy = pro,
                                                num = num,
                                                yagooglesearch_manages_http_429s = False,
                                                minimum_delay_between_paged_results_in_seconds = 7
                                                )
                )
            self._search_manager = AutoManagementProxy(self._search_manager)


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

    @property
    def period(self):
        return self._period

    @period.setter
    def period(self, per):
        try:
            Time(per)
            self._period = per
        except Exception as ex:
            raise ExceptionCountryFormat(f'The search country is incorrect: {ex}')

    @property
    def search_manager(self):
        return self._search_manager

    @period.setter
    def proxy(self, pro):
        if pro is None:
            self._search_manager = None
        else:
            self._proxy = AutoManagementProxy(pro)

    def get_status_settings(self, type_search):
        if TypeSearch[type_search].value == 2:
            translator = Translator()
            data = translator.translate(self._text, dest = str(self._language).split('lang_')[1])
            self._text = data.text

    @staticmethod
    def get_data(text, search_manager):
        data = ManageGoogleSearch().get_search_results(text = text, search_manager = search_manager)
        return data

    def get_google_dork(self, text):
        return self.get_data(text = f'{text}', )

    def get_facebook(self, text):
        return self.get_data(text = f'site:facebook.com {text}',)

    def get_twitter(self, text):
        return self.get_data(text = f'site:twitter.com {text}',)

    def get_vk(self, text):
        return self.get_data(text = f'site:vk.com {text}',)

    def get_discord(self, text):
        return self.get_data(text = f'site:vk.com {text}', search_manager = self._search_manager)

    def get_discord(self, text):
        return self.get_data(text = f'site:discord.com {text}', )

    def get_instagram(self, text):
        return self.get_data(text = f'site:www.instagram.com {text}', search_manager = self._search_manager)

    def get_instagram_hashtag(self, text):
        return self.get_data(text = f'site:www.instagram.com #{text}', search_manager = self._search_manager)

    def get_instagram_reels(self, text):
        return self.get_data(text = f'site:https://www.instagram.com inurl:reels #{text}', search_manager = self._search_manager)

    def get_youtube(self, text):
        return self.get_data(text = f'site:youtube.com {text}', search_manager = self._search_manager)


class ManageGoogleSearch:

    def error_handling(self, url, search_manager):
        logger.info('Waiting for collection for 30 minutes')
        time.sleep(1800)
        logger.info('Waiting for collection for 30 minutes')
        logger.info("HTTP 429 detected...it's up to you to modify your search.")
        url.remove("HTTP_429_DETECTED")
        one_manager = search_manager.get_proxy()
        logger.info(one_manager)
        url = url + one_manager.search()
        if "HTTP_429_DETECTED" in url:
            self.error_handling(url, search_manager)
        url.remove("HTTP_429_DETECTED")
        url.info("URLs found before HTTP 429 detected...")
        for link in url:
            url.append(link)
        return link


    def get_search_results(self, text,search_manager):
        urls = []
        one_manager = search_manager.get_proxy()
        one_manager.query = text
        one_manager.update_urls()
        logger.info(one_manager.query)
        logger.info(one_manager.proxy)
        one_manager.assign_random_user_agent()
        url_collection = one_manager.search()
        logger.info(url_collection)
        time.sleep(100)
        if "HTTP_429_DETECTED" in url_collection:
            url_collection = self.error_handling(url_collection, one_manager)

        for link in url_collection:
            urls.append(link)
        return urls


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
