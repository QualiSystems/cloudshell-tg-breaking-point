from cloudshell.shell.core.driver_context import AutoLoadDetails
from cloudshell.tg.breaking_point.autoload.info.bp_ports_info import BPPortsInfo
from cloudshell.tg.breaking_point.flows.bp_flow import BPFlow
from cloudshell.tg.breaking_point.rest_actions.autoload_actions import AutoloadActions


class BPAutoloadFlow(BPFlow):
    def autoload_details(self):
        elements = {}
        with self._session_manager.get_session() as session:
            autoload_actions = AutoloadActions(session, self._logger)
            ports_info = BPPortsInfo(autoload_actions, self._logger)
            elements.update(ports_info.collect())
            self._connect_elements(elements)
            details = self._build_autoload_details(elements)
            return details

    @staticmethod
    def _connect_elements(elements):
        for element in elements.values():
            if element.parent_id and element.parent_id in elements:
                element.add_parent(elements.get(element.parent_id))

    @staticmethod
    def _build_autoload_details(elements):
        resources = []
        attributes = []
        for element in elements.values():
            attributes.extend(element.autoload_attributes)
            if element.relative_address:
                resources.append(element.autoload_resource())

        return AutoLoadDetails(resources, attributes)
