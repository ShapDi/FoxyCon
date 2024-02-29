import re

import requests


BASE_URL = 'https://www.instagram.com/'
MEDIA_URL = BASE_URL + 'p/{0}/?__a=1'

QUERY_HASHTAG = BASE_URL + \
                'graphql/query/?query_hash=ded47faa9a1aaded10161a2ff32abb6b&variables={0}'
QUERY_HASHTAG_VARS = '{{"tag_name":"{0}","first":{1},"after":"{2}"}}'

CHROME_WIN_UA = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 ' \
                '(KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'


class DataInstagramHashtag:
    def __init__(self):
        self.items = []
        self.session = requests.Session()
        self.session.headers = {'user-agent': CHROME_WIN_UA}
        self.session.cookies.set('ig_pr', '1')
        self.rhx_gis = None

    def scrape_hashtag(self, hashtag, end_cursor = '', maximum = 10, first = 10,
                       initial = True, detail = False, proxy = []):

        if proxy != []:
            self.session.proxies = proxy

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
                date_results.append({'text':f'{text}',
                                     'link':f"https://www.instagram.com/p/{element.get('shortcode')}",
                                     'caption': hashtags})
        return date_results


scraper = DataInstagramHashtag()
print(scraper.get_data('1xbet', max_results = 100))

