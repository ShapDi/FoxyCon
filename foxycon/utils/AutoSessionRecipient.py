import time


from loguru import logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class AutomaticSessionRecipient:
    def __init__(self, username = None, password = None):
        self._username = username
        self._password = password

    def get_instagram(self):
        return InstagramSessionRecipient.get_cookies(username = self._username, password = self._password)

    def get_google(self):
        return GoogleSessionRecipient.get_cookies()

class InstagramSessionRecipient:

    @classmethod
    def get_drive(cls):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument("--disable-blink-features=AutomationControlled")
        driver = webdriver.Chrome(options = options)
        return driver

    @classmethod
    def get_cookies(cls, username, password):
        driver = cls.get_drive()
        driver.get("https://www.instagram.com/")
        time.sleep(10)
        login = driver.find_element(By.CSS_SELECTOR,
                                         """#loginForm > div > div:nth-child(1) > div > label > input""")
        login.clear()
        login.send_keys(f"{username}")
        password = driver.find_element(By.CSS_SELECTOR,
                                            """#loginForm > div > div:nth-child(2) > div > label > input""")
        password.clear()
        password.send_keys(f"{password}")
        ent = driver.find_element(By.CSS_SELECTOR, """#loginForm > div > div:nth-child(3) > button""")
        ent.send_keys(Keys.ENTER)
        sessionid = driver.get_cookie(name='sessionid').get('value')
        return sessionid


class GoogleSessionRecipient:

    @classmethod
    def get_drive(cls):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument("--disable-blink-features=AutomationControlled")
        driver = webdriver.Chrome(options = options)
        return driver

    @staticmethod
    def clearing_cookies(cookies):
        new_cookies = ""
        for cook in cookies:
            new_cookies = new_cookies + f"{cook.get('name')}:{cook.get('value')}"
            # new_cookies[cook.get('name')] = cook.get('value')
        return new_cookies
    @classmethod
    def get_cookies(cls):
        driver = cls.get_drive()
        driver.get("https://www.google.com/")
        time.sleep(5)
        cookies = driver.get_cookies()
        cookies = cls.clearing_cookies(cookies)
        return cookies




