from abc import ABCMeta

from cloudshell.tg.breaking_point.rest_api.rest_session_manager import RestSessionContextManager


class BPRunner(object):
    __metaclass__ = ABCMeta

    def __init__(self, session_credentials, logger):
        self.__session_credentials = session_credentials
        self.logger = logger
        self.__session_context_manager = None

    def _set_session_credentials(self, value):
        self.__session_credentials = value
        if self.__session_context_manager:
            self.__session_context_manager.set_session_credentials(value)

    @property
    def _session_context_manager(self):
        if not self.__session_context_manager:
            self.__session_context_manager = RestSessionContextManager(self.__session_credentials, self.logger)
        return self.__session_context_manager
