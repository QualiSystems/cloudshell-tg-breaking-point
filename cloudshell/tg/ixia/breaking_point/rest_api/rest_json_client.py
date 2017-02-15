from cloudshell.tg.ixia.breaking_point.rest_api.rest_requests import RestRequests
import requests

requests.packages.urllib3.disable_warnings()


class RestClientUnauthorizedException(Exception):
    pass


class RestClientException(Exception):
    pass


class RestJsonClient(RestRequests):
    def __init__(self, hostname, use_https=True):
        self._cookies = None
        self._hostname = hostname
        self._use_https = use_https
        self._session = requests.Session()

    def _build_url(self, uri):
        if self._hostname not in uri:
            if not uri.startswith('/'):
                uri = '/' + uri
            if self._use_https:
                url = 'https://{0}{1}'.format(self._hostname, uri)
            else:
                url = 'http://{0}{1}'.format(self._hostname, uri)
        else:
            url = uri
        return url

    def request_put(self, uri, data):
        response = self._session.put(self._build_url(uri), data, cookies=self._cookies, verify=False)
        if response.status_code in [200, 201, 204]:
            return response.json()
        elif response.status_code in [401]:
            raise RestClientUnauthorizedException(self.__class__.__name__, 'Incorrect login or password')
        else:
            raise RestClientException(self.__class__.__name__,
                                      'Request put failed: {0}, {1}'.format(response.status_code, response.reason))

    def request_post(self, uri, data):
        response = self._session.post(self._build_url(uri), json=data, cookies=self._cookies, verify=False)
        if response.status_code in [200, 201]:
            return response.json()
        elif response.status_code in [401]:
            raise RestClientUnauthorizedException(self.__class__.__name__, 'Incorrect login or password')
        else:
            raise RestClientException(self.__class__.__name__,
                                      'Request post failed: {0}, {1}'.format(response.status_code, response.reason))

    def request_get(self, uri):
        response = self._session.get(self._build_url(uri), cookies=self._cookies, verify=False)
        if response.status_code in [200]:
            return response.json()
        elif response.status_code in [401]:
            raise RestClientUnauthorizedException(self.__class__.__name__, 'Incorrect login or password')
        else:
            raise RestClientException(self.__class__.__name__,
                                      'Request get failed: {0}, {1}'.format(response.status_code, response.reason))

    def request_delete(self, uri):
        response = self._session.delete(self._build_url(uri), cookies=self._cookies, verify=False)
        if response.status_code in [200, 204]:
            return response.content
        elif response.status_code in [401]:
            raise RestClientUnauthorizedException(self.__class__.__name__, 'Incorrect login or password')
        else:
            raise RestClientException(self.__class__.__name__,
                                      'Request delete failed: {0}, {1}'.format(response.status_code, response.reason))
