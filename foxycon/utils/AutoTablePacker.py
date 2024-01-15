import pandas as pd

from foxycon.search_services.AutoAdsLibrary.DataFBAdsLib import DataFBAdsLib


class AutoTablePacker:
    def __init__(self, name, path, data):
        self._name = name
        self._path = path
        self._data = data

    def get_facebook_ads(self):
        return FacebookTablePacker.get_table(self._data)


class FacebookTablePacker:

    @staticmethod
    def get_table(data):
        df = pd.DataFrame(columns=list(data[0].keys()))
        for one in data:
            df.loc[len(df.index)] = list(one.values())
        df.to_excel('./teams.xlsx')


