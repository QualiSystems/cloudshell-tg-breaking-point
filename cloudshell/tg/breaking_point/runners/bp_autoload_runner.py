from cloudshell.tg.breaking_point.flows.bp_autoload_flow import BPAutoloadFlow
from cloudshell.tg.breaking_point.runners.bp_runner import BPRunner


class BPAutoloadRunner(BPRunner):
    def __init__(self, context, logger, api, supported_os):
        super(BPAutoloadRunner, self).__init__(context, logger, api)
        self._supported_os = supported_os

    @property
    def _autoload_flow(self):
        return BPAutoloadFlow(self._session_manager, self.logger)

    def discover(self):
        return self._autoload_flow.autoload_details()
