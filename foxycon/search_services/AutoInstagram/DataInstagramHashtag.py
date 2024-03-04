import re

import requests

from foxycon.utils import AutoManagementProxy

BASE_URL = 'https://www.instagram.com/'
MEDIA_URL = BASE_URL + 'p/{0}/?__a=1'

QUERY_HASHTAG = BASE_URL + \
                'graphql/query/?query_hash=ded47faa9a1aaded10161a2ff32abb6b&variables={0}'
QUERY_HASHTAG_VARS = '{{"tag_name":"{0}","first":{1},"after":"{2}"}}'

CHROME_WIN_UA = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 ' \
                '(KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'

ip_list_india = [
    'http://XpchYn:HtatoG@5.101.34.75:8000',
    'http://XpchYn:HtatoG@5.101.34.192:8000',
    'http://XpchYn:HtatoG@5.101.34.108:8000',
    'http://XpchYn:HtatoG@5.101.34.4:8000',
    'http://XpchYn:HtatoG@5.101.34.122:8000'
]

proxy_list = [
    "http://c060c353:6f33c6c151@185.64.250.158:30010",
    "http://c060c353:6f33c6c151@185.64.250.191:30010",
    "http://c060c353:6f33c6c151@85.31.51.154:30010",
    "http://c060c353:6f33c6c151@85.31.50.115:30010",
    "http://c060c353:6f33c6c151@85.31.48.157:30010",
]

proxy = AutoManagementProxy(proxy = proxy_list)



class DataInstagramHashtag:
    def __init__(self, proxy:AutoManagementProxy = []):
        self.items = []
        self.session = requests.Session()
        self.rhx_gis = None
        self.proxy = proxy

    def scrape_hashtag(self, hashtag, end_cursor = '', maximum = 10, first = 10,
                       initial = True, detail = False):

        self.session.headers = {'user-agent': CHROME_WIN_UA}
        self.session.cookies.set('ig_pr', '1')

        if self.proxy != []:
            self.session.proxies = {'https': self.proxy.get_proxy()}


        if initial:
            self.items = []

        try:
            params = QUERY_HASHTAG_VARS.format(hashtag, 10, end_cursor)
            response = self.session.get(QUERY_HASHTAG.format(params)).json()
            data = response['data']['hashtag']
        except Exception as ex:
            print(ex)
            self.session.close()
            return []

        if data:
            for item in data['edge_hashtag_to_media']['edges']:
                node = item['node']
                caption = None
                if node['edge_media_to_caption']['edges']:
                    caption = node[
                        'edge_media_to_caption']['edges'][0]['node']['text']

                if any([detail, node['is_video']]):
                    try:
                        r = requests.get(MEDIA_URL.format(
                            node['shortcode'])).json()
                    except Exception:
                        continue

                if node['is_video']:
                    display_url = r['graphql']['shortcode_media']['video_url']
                else:
                    display_url = node['display_url']

                item = {
                    'is_video': node['is_video'],
                    'caption': caption,
                    'display_url': display_url,
                    'thumbnail_src': node['thumbnail_src'],
                    'owner_id': node['owner']['id'],
                    'id': node['id'],
                    'shortcode': node['shortcode'],
                    'taken_at_timestamp': node['taken_at_timestamp']
                }

                if detail:
                    owner = r['graphql']['shortcode_media']['owner']
                    item['profile_picture'] = owner['profile_pic_url']
                    item['username'] = owner['username']

                if item not in self.items and len(self.items) < maximum:
                    self.items.append(item)

            end_cursor = data[
                'edge_hashtag_to_media']['page_info']['end_cursor']
            if end_cursor and len(self.items) < maximum:
                self.scrape_hashtag(hashtag, detail = detail, initial = False,
                                    end_cursor = end_cursor, maximum = maximum)
        self.session.close()

        return self.items

    def get_data(self, text, max_results):
        date_results = []
        data = self.scrape_hashtag(text, maximum = max_results)
        if data == []:
            return 'No results'
        else:
            for element in data:
                if element.get('caption') is None:
                    hashtags = 'There are no hashtags'
                else:
                    hashtags = re.findall(r'\#\w+', element.get('caption'))
                print(element)
                date_results.append({'text': f'{text}',
                                     'link': f"https://www.instagram.com/p/{element.get('shortcode')}",
                                     'caption': hashtags,
                                     'photo':element.get('thumbnail_src')})
        return date_results


# scraper = DataInstagramHashtag(proxy = proxy)
# print(scraper.get_data('india', max_results = 100))
