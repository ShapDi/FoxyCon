from abc import ABC, abstractmethod
from enum import Enum
import re


class ContentTypeAbstract(ABC):
    @abstractmethod
    def get_type_publication(self): pass


class ContentTypeFacebook(ContentTypeAbstract):
    def __init__(self, weight):
        self._weight = weight
    def get_type_publication(self):
        weight = re.split(r'/', self._weight)
        result = ''
        for type in Facebook:
            if type.name in weight:
                result = Facebook[type.name].value
                break
            else:
                result = Facebook['page'].value
        return result

    @classmethod
    def __repr__(cls):
        return "facebook"


class ContentTypeInstagram(ContentTypeAbstract):

    def __init__(self, weight):
        self._weight = weight

    def get_type_publication(self):
        weight = re.split(r'/', self._weight)
        result = ''
        for type in Instagram:
            if type.name in weight:
                result = Instagram[type.name].value
                break
            else:
                result = Instagram['page'].value
        return result

    @classmethod
    def __repr__(cls):
        return "instagram"


class ContentTypeVK(ContentTypeAbstract):
    def __init__(self, weight):
        self._weight = weight
    def get_type_publication(self):
        weight = re.split(r'/', self._weight)
        result = ''
        for type in VK:
            if type.name in weight:
                result = VK[type.name].value
                break
            elif type.name in re.split(r'-', weight[1]):
                result = VK[type.name].value
                break
            else:
                result = VK['page'].value
        return result
    @classmethod
    def __repr__(cls):
        return "vk"



class ContentTypeTwitter(ContentTypeAbstract):
    def __init__(self, weight):
        self._weight = weight
    def get_type_publication(self):
        weight = re.split(r'/', self._weight)
        result = ''
        for type in Twitter:
            if type.name in weight:
                result = Twitter[type.name].value
                break
            else:
                result = Twitter['page'].value
        return result
    @classmethod
    def __repr__(cls):
        return "twitter"


class Facebook(Enum):
    groups = 'groups'
    photo = 'photo'
    page = 'page'

class Instagram(Enum):
    reel = 'reel'
    p = 'post'
    page = 'page'


class Twitter(Enum):
    page = 'page'
    status = 'post'

class VK(Enum):
    reel = 'reel'
    wall = 'post'
    page = 'page'
    photo = 'photo'

class YouTube(Enum):
    shorts = 'shorts'
    video = 'video'
    channel = 'channel'

class DataAnalyzer:
    CONTENTANALYZERS = {cl.__repr__(): cl for cl in ContentTypeAbstract.__subclasses__()}

    def __init__(self, link):
        self._link = link

    @staticmethod
    def get_social_media(link):
        match = re.split(r'(?:[-\w]+\.)?([-\w]+)\.\w+(?:\.\w+)?', link)
        return [match[1], match[2]]

    @classmethod
    def get_type_post(cls, social_media, weight):
        social_media = cls.CONTENTANALYZERS.get(social_media)
        return social_media(weight).get_type_publication()

    def get_result(self):
        data = self.get_social_media(self._link)
        type_post = self.get_type_post(data[0], data[1])
        return {'social_media': data[0], "type": type_post}

