from threading import Lock

from cloudshell.tg.breaking_point.rest_actions.auth_actions import AuthActions
from cloudshell.tg.breaking_point.rest_api.rest_json_client import RestJsonClient


class RestSessionContextManager(object):
    def __init__(self, hostname, username, password, logger):
        self.__lock = Lock()
        self._hostname = hostname
        self._username = username
        self._password = password
        self._logger = logger
        self.__session = None
        self.__auth_actions = None

    @property
    def _session(self):
        if not self.__session:
            self.__session = RestJsonClient(self._hostname)
        return self.__session

    @property
    def _auth_actions(self):
        if not self.__auth_actions:
            self.__auth_actions = AuthActions(self._session, self._logger)
        else:
            self.__auth_actions.logger = self._logger
        return self.__auth_actions

    def __del__(self):
        if self.__auth_actions:
            self.__auth_actions.logout()

    def __enter__(self):
        """

        :return:
        :rtype: RestJsonClient
        """
        self.__lock.acquire()
        if not self._auth_actions.logged_in():
            self._auth_actions.login(self._username, self._password)
        return self._session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__lock.release()
        # self._auth_actions.logout()


class RestSessionManager(object):
    def __init__(self, resource_address, username, password, logger):
        """
        :param resource_address:
        :param username:
        :param password:
        :param logger:
        """
        self.__session_context_manager = None
        self._resource_address = resource_address
        self._username = username
        self._password = password
        self._logger = logger

    def get_session(self):
        if not self.__session_context_manager:
            self.__session_context_manager = RestSessionContextManager(self._resource_address, self._username,
                                                                       self._password, self._logger)
        return self.__session_context_manager
