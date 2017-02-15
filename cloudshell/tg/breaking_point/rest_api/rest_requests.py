from abc import ABCMeta, abstractmethod


class RestRequests(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def request_get(self, uri):
        pass

    @abstractmethod
    def request_post(self, uri, data):
        pass

    @abstractmethod
    def request_put(self, uri, data):
        pass

    @abstractmethod
    def request_delete(self, uri):
        pass
