from cloudshell.tg.ixia.breaking_point.autoload.model.bp_chassis_entities import Chassis
from cloudshell.tg.ixia.breaking_point.rest_actions.autoload_actions import AutoloadActions


class BPChassisInfo(object):
    PREFIX = 'CH'
    ID = 0

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
        self._logger.debug('Collecting chassis info')
        unique_id = self.PREFIX + str(self.ID)
        chassis = Chassis(self.ID, unique_id)
        return {unique_id: chassis}
