from cloudshell.shell.core.context_utils import get_attribute_by_name, get_resource_address
from cloudshell.tg.ixia.breaking_point.rest_actions.auth_actions import AuthActions
from cloudshell.tg.ixia.breaking_point.rest_api.rest_json_client import RestJsonClient


class RestSessionContextManager(object):
    def __init__(self, hostname, username, password, logger):
        self._hostname = hostname
        self._username = username
        self._password = password
        self._logger = logger
        self._session = RestJsonClient(self._hostname)
        self._auth_actions = AuthActions(self._session, self._logger)

    def __enter__(self):
        self._auth_actions.login(self._username, self._password)
        return self._session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._auth_actions.logout()


class RestSessionManager(object):
    def __init__(self, context, logger, api):
        self._context = context
        self._logger = logger
        self._api = api

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

    def new_session(self):
        return RestSessionContextManager(self._resource_address, self._username, self._password, self._logger)
