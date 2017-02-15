from cloudshell.shell.core.context_utils import get_attribute_by_name, get_resource_address
from cloudshell.tg.breaking_point.flows.bp_autoload_flow import BPAutoloadFlow
from cloudshell.tg.breaking_point.rest_api.rest_session_manager import RestSessionManager


class BPAutoloadRunner(object):
    def __init__(self, context, logger, api, supported_os):
        self._context = context
        self._api = api
        self._logger = logger
        self._supported_os = supported_os

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
        return RestSessionManager(self._resource_address, self._username, self._password, self._logger)

    @property
    def _autoload_flow(self):
        return BPAutoloadFlow(self._session_manager, self._logger)

    def discover(self):
        return self._autoload_flow.autoload_details()
