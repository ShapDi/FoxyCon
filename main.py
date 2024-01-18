from foxycon.search_services import DataFBAdsLib, CountryAds
from foxycon.utils.AutoTablePacker import AutoTablePacker
from foxycon.search_services import DataGoogleSearch, LanguageGoogle, TimeGoogle, CountryGoogle

# data = DataGoogleSearch(language = 'lang_e', country = 'CA', period = 'year')

# Нужно найти воронки по гео чили перу Аргентина Колумбия Бангладеш
# Суть рекламы будет «заработай со мной»
# И дальше реклама ведет в телеграмм канал , aviator

# serch = ['aviator', 'make money with me', 'ganhar dinheiro comigo', 'ganar dinero conmigo']
# data = []
#
# for i in serch:
#     data_fb = DataFBAdsLib(text = i, country = CountryAds.Argentina).get_data()
#     data = data + data_fb
#     data_fb = DataFBAdsLib(text = i, country = CountryAds.Brazi).get_data()
#     data = data + data_fb
#     data_fb = DataFBAdsLib(text = i, country = CountryAds.Peru).get_data()
#     data = data + data_fb
#
# AutoTablePacker(name = 'table', path = 'C:\git\FoxyCon', data = data).get_facebook_ads()
#


ip_list = [
    'http://zjMKKB:3ru9Pn@185.39.149.135:8000',
    'http://zjMKKB:3ru9Pn@91.216.59.86:8000'
]
dad = DataGoogleSearch(language = LanguageGoogle.english.value,
                       country = CountryGoogle.india.value,
                       period = TimeGoogle.week.value,
                       num = 400,
                       proxy = ip_list,
                       type_search = 'standard')

reqvest = ['mostbet','1xbet', 'parimatch']

for i in reqvest:
    print(dad.get_instagram(i))
