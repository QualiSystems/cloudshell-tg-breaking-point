from cloudshell.tg.breaking_point.autoload.model.bp_chassis_entities import Chassis
from cloudshell.tg.breaking_point.rest_actions.autoload_actions import AutoloadActions


class BPChassisInfo(object):
    PREFIX = 'CH'

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
        unique_id = self.PREFIX
        chassis = Chassis(None, unique_id)
        return {unique_id: chassis}
