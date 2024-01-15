import collections

class AutoManagementProxy:
    def __init__(self, proxy:list):
        self._proxy = collections.deque(proxy)


    def get_proxy(self):
        element = self._proxy.popleft()
        proxy = element
        self._proxy.append(element)
        return proxy



