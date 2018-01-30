from threading import Lock

from cloudshell.tg.breaking_point.rest_actions.auth_actions import AuthActions
from cloudshell.tg.breaking_point.rest_api.rest_json_client import RestJsonClient


class RestSessionContextManager(object):
    def __init__(self, session_credentials, logger):
        """

        :param session_credentials:
        :type session_credentials: cloudshell.tg.breaking_point.rest_api.rest_session_credentials.RestSessionCredentials
        :param logger:
        """
        self.__lock = Lock()
        self.__session_credentials = session_credentials
        self._logger = logger
        self.__session = None
        self.__auth_actions = None

    def set_session_credentials(self, session_credentials):
        if self.__session_credentials != session_credentials:
            self.__session_credentials = session_credentials
            self._destroy_session()

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, logger):
        self._logger = logger

    @property
    def _session(self):
        if not self.__session:
            self.__session = RestJsonClient(self.__session_credentials.hostname)
        return self.__session

    @property
    def _auth_actions(self):
        if not self.__auth_actions:
            self.__auth_actions = AuthActions(self._session, self._logger)
        return self.__auth_actions

    def _destroy_session(self):
        if self.__auth_actions:
            self.__auth_actions.logout()
            self.__session = None
            self.__auth_actions = None

    def __del__(self):
        self._destroy_session()

    def __enter__(self):
        """
        :return:
        :rtype: RestJsonClient
        """
        self.__lock.acquire()
        if not self._auth_actions.logged_in():
            try:
                self._auth_actions.login(self.__session_credentials.username, self.__session_credentials.password)
            except:
                self.__lock.release()
                raise
        return self._session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__lock.release()
