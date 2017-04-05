from abc import ABCMeta
from cloudshell.shell.core.context_utils import get_attribute_by_name, get_resource_address
from cloudshell.tg.breaking_point.rest_api.rest_session_manager import RestSessionManager


class BPRunner(object):
    __metaclass__ = ABCMeta

    def __init__(self, context, logger, api):
        self.__context = context
        self.__api = api
        self.__logger = logger

        self.__session_manager = None

    @property
    def _context(self):
        return self.__context

    @_context.setter
    def _context(self, value):
        self.__context = value

    @property
    def _logger(self):
        return self.__logger

    @_logger.setter
    def _logger(self, value):
        self.__logger = value

    @property
    def _api(self):
        return self.__api

    @_api.setter
    def _api(self, value):
        self.__api = value

    @property
    def _username(self):
        return get_attribute_by_name('User', self._context)

    @property
    def _password(self):
        password = get_attribute_by_name(attribute_name='Password', context=self._context)
        return self._api.DecryptPassword(password).Value

    @property
    def _resource_address(self):
        """Resource IP

        :return:
        """
        return get_resource_address(self._context)

    @property
    def _session_manager(self):
        if not self.__session_manager:
            self.__session_manager = RestSessionManager(self._resource_address, self._username, self._password,
                                                        self._logger)
        return self.__session_manager
