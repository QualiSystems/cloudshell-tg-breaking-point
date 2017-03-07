from abc import ABCMeta
from cloudshell.shell.core.context_utils import get_attribute_by_name, get_resource_address
from cloudshell.tg.breaking_point.rest_api.rest_session_manager import RestSessionManager


class BPRunner(object):
    __metaclass__ = ABCMeta

    def __init__(self, context, logger, api):
        self._context = context
        self._api = api
        self._logger = logger
        self._session_manager = None

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, value):
        self._context = value

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, value):
        self._logger = value

    @property
    def api(self):
        return self._api

    @api.setter
    def api(self, value):
        self._api = value

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
    def session_manager(self):
        if not self._session_manager:
            self._session_manager = RestSessionManager(self._resource_address, self._username, self._password,
                                                       self._logger)
        return self._session_manager
