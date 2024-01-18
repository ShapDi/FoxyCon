import re
import time
from enum import Enum

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


class DataFBAdsLib:

    def __init__(self, country, text):
        self._country = country
        self._text = text

    @staticmethod
    def get_html(country, text):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        options.add_argument('headless')
        options.add_argument("--disable-blink-features=AutomationControlled")
        driver = webdriver.Chrome(service = ChromeService(ChromeDriverManager().install()), options = options)
        driver.get(
            f"""https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country={country}&q=
            {text}&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped
            &search_type=keyword_exact_phrase&media_type=all""")
        time.sleep(5)
        data = driver.page_source
        driver.close()

        return data

    @staticmethod
    def get_data_banners(name, data):
        soup = BeautifulSoup(data, "html5lib")
        baners = soup.find_all(class_ = '_7jvw x2izyaf x1hq5gj4 x1d52u69')
        data = []
        for baner in baners:
            text = [i for i in re.split("===", baner.get_text(separator = "===")) if i != '\u200b']
            text = HandlerBanner().get_data_text(name, text)
            link = HandlerBanner().get_data_link([link.get('href') for link in baner.find_all(name = 'a')])
            data.append(text | link)
        return data

    def get_data(self):
        data = self.get_html(self._country, self._text)
        data = self.get_data_banners(self._text, data)
        return data


class HandlerBanner:

    def get_id(self, line):
        line = line[0].split(':')
        data = {'ID': line[1], 'LinkAdsLibrary': f'https://www.facebook.com/ads/library/?id={line[1].split(" ")[1]}'}
        return data

    def get_date(self, line):
        data = {'date': line[2]}
        return data

    def get_activity(self, line):
        data = {"activity": line[1]}
        return data

    def get_usage(self, line):
        data = line[4] + line[5]
        data = {'usage': data}
        return data

    def get_description(self, line):
        text = line[10:-1]
        data = ""
        for word in text:
            data = data + str(word)
        data = {'description': data}
        return data

    def get_link_group(self, text):
        data = {'link_group': text[0]}
        return data

    def get_goal_ads(self, text):
        try:
            data = {'goal_ads': text[1]}
        except:
            data = {'goal_ads': "no"}
        return data

    def get_data_text(self, name, country, text):
        data = {'request': name}
        data.update({'country': Country[country]})
        data.update(self.get_id(text))
        data.update(self.get_date(text))
        data.update(self.get_activity(text))
        data.update(self.get_usage(text))
        data.update(self.get_description(text))
        return data

    def get_data_link(self, links):
        data = self.get_link_group(links)
        goal_ads = self.get_goal_ads(links)
        data.update(goal_ads)
        return data


class Country(Enum):
    Canada = 'CA'
    Peru = 'PE'
    Argentina = 'AR'
    Colombia = 'CO'
    Bangladesh = 'BD'
    Brazi = 'BZ'
