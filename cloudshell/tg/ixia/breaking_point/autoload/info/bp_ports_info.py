from cloudshell.tg.ixia.breaking_point.autoload.info.bp_modules_info import BPModulesInfo
from cloudshell.tg.ixia.breaking_point.autoload.model.bp_chassis_entities import Port
import re
from cloudshell.tg.ixia.breaking_point.rest_actions.autoload_actions import AutoloadActions


class BPPortsInfo(object):
    PREFIX = 'PORT'

    def __init__(self, autoload_actions, logger):
        """
        :param autoload_actions:
        :type autoload_actions: AutoloadActions
        :param logger:
        :return:
        """
        self.autoload_actions = autoload_actions
        self._logger = logger

    # u'{[slot=1,port=1]=1, [slot=1,port=0]=0}'
    #     u'{[slot=1,port=1]=1, [slot=1,port=0]=0:[reserved=admin,group=1,number=1]}'
    def collect(self):
        self._logger.debug('Collecting ports info')
        ports_info = self.autoload_actions.get_ports_info()
        data = re.findall(r'\[slot=(\d+),port=(\d+)\]', ports_info)
        ports = {}
        for mod_id, port_id in data:
            parent_unique_id = BPModulesInfo.PREFIX + str(mod_id)
            unique_id = parent_unique_id + self.PREFIX + str(port_id)
            ports[unique_id] = Port(port_id, unique_id, parent_id=parent_unique_id)
        return ports
