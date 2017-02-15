from cloudshell.tg.ixia.breaking_point.flows.bp_autoload_flow import BPAutoloadFlow
from cloudshell.tg.ixia.breaking_point.rest_api.rest_session_manager import RestSessionManager


class BPAutoloadRunner(object):
    def __init__(self, context, logger, api, supported_os):
        self._context = context
        self._api = api
        self._logger = logger
        self._supported_os = supported_os

    @property
    def _session_manager(self):
        return RestSessionManager(self._context, self._logger, self._api)

    @property
    def _autoload_flow(self):
        return BPAutoloadFlow(self._session_manager, self._logger)

    def discover(self):
        return self._autoload_flow.autoload_details()
