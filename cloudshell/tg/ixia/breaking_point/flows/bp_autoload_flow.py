from cloudshell.shell.core.driver_context import AutoLoadDetails
from cloudshell.tg.ixia.breaking_point.autoload.info.bp_chassis_info import BPChassisInfo
from cloudshell.tg.ixia.breaking_point.autoload.info.bp_modules_info import BPModulesInfo
from cloudshell.tg.ixia.breaking_point.autoload.info.bp_ports_info import BPPortsInfo
from cloudshell.tg.ixia.breaking_point.rest_actions.autoload_actions import AutoloadActions
from cloudshell.tg.ixia.breaking_point.rest_api.rest_session_manager import RestSessionManager


class BPAutoloadFlow(object):
    def __init__(self, session_manager, logger):
        """
        :param session_manager:
        :type session_manager: RestSessionManager
        :param logger:
        :return:
        """
        self._session_manager = session_manager
        self._logger = logger
        self._elements = {}

    def autoload_details(self):
        with self._session_manager.new_session() as session:
            autoload_actions = AutoloadActions(session, self._logger)

            chassis_info = BPChassisInfo(autoload_actions, self._logger)
            self._elements.update(chassis_info.collect())

            modules_info = BPModulesInfo(autoload_actions, self._logger)
            self._elements.update(modules_info.collect())

            ports_info = BPPortsInfo(autoload_actions, self._logger)
            self._elements.update(ports_info.collect())
            self._connect_elements()
            details = self._build_autoload_details()
            return details

    def _connect_elements(self):
        for element in self._elements.values():
            if element.parent_id and element.parent_id in self._elements:
                element.add_parent(self._elements.get(element.parent_id))

    def _build_autoload_details(self):
        resources = self._elements.values()
        attributes = []
        for resource in resources:
            attributes.extend(resource.attributes)
        return AutoLoadDetails(resources, attributes)
