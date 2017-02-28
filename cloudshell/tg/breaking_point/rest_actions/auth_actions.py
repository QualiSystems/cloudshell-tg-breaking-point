from cloudshell.tg.breaking_point.rest_api.rest_json_client import RestJsonClient, RestClientUnauthorizedException


class AuthActions(object):
    def __init__(self, rest_service, logger):
        """
        Reboot actions
        :param rest_service:
        :type rest_service: RestJsonClient
        :param logger:
        :type logger: Logger
        :return:
        """
        self._rest_service = rest_service
        self._logger = logger

    def login(self, username, password):
        """
        Login request
        :param username:
        :param password:
        :return:
        """
        self._logger.debug('Login request with  Username: {0}, Password: {1}'.format(username, password))
        uri = '/api/v1/auth/session'
        json_data = {'username': username, 'password': password}
        self._rest_service.request_post(uri, json_data)

    def logout(self):
        """
        Logout request
        :return:
        """
        self._logger.debug('Logout request')
        uri = '/api/v1/auth/session'
        self._rest_service.request_delete(uri)

    def logged_in(self):
        """
        Check if logged-in
        :return:
        """
        self._logger.debug('Check logged-in request')
        uri = '/api/v1/bps/'
        logged_in = False
        try:
            self._rest_service.request_get(uri)
            logged_in = True
        except RestClientUnauthorizedException:
            pass
        return logged_in
