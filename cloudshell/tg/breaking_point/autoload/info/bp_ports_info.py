from cloudshell.tg.breaking_point.autoload.info.bp_modules_info import BPModulesInfo
from cloudshell.tg.breaking_point.autoload.model.bp_chassis_entities import Port, Module
import re
from cloudshell.tg.breaking_point.rest_actions.autoload_actions import AutoloadActions


class BPPortsInfo(object):
    PORT_PREFIX = 'PORT'
    MOD_PREFIX = 'MOD'

    def __init__(self, autoload_actions, logger):
        """
        :param autoload_actions:
        :type autoload_actions: AutoloadActions
        :param logger:
        :return:
        """
        self.autoload_actions = autoload_actions
        self._logger = logger

    def collect(self):
        self._logger.debug('Collecting ports info')
        ports_info = self.autoload_actions.get_ports_info()
        data = re.findall(r'\[slot=(\d+),port=(\d+)\]', ports_info)
        elements = {}
        for mod_id, port_id in data:
            mod_unique_id = self.MOD_PREFIX + str(mod_id)
            port_unique_id = mod_unique_id + self.PORT_PREFIX + str(port_id)
            if mod_unique_id not in elements:
                elements[mod_unique_id] = Module(mod_id, mod_unique_id, parent_id=None)
            elements[port_unique_id] = Port(port_id, port_unique_id, parent_id=mod_unique_id)
        return elements
