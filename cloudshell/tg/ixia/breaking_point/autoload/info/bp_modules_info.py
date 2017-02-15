from cloudshell.tg.ixia.breaking_point.autoload.info.bp_chassis_info import BPChassisInfo
from cloudshell.tg.ixia.breaking_point.autoload.model.bp_chassis_entities import Module
from cloudshell.tg.ixia.breaking_point.rest_actions.autoload_actions import AutoloadActions


class BPModulesInfo(object):
    PREFIX = 'MOD'

    def __init__(self, autoload_actions, logger):
        """
        :param autoload_actions:
        :type autoload_actions: AutoloadActions
        :param logger:
        :return:
        """
        self.autoload_actions = autoload_actions
        self._logger = logger

    # {u'1': {u'state': u'ok', u'portSpeed': 10000, u'model': u'BPS-VE', u'performanceAccelerationEnabled': False}}

    def collect(self):
        self._logger.debug('Collecting modules info')
        modules_dict = {}
        info_dict = self.autoload_actions.get_modules_info()
        for module_id, module_info in info_dict.iteritems():
            unique_id = self.PREFIX + module_id
            module = Module(module_id, unique_id, parent_id=BPChassisInfo.PREFIX + str(BPChassisInfo.ID))
            module.device_model = module_info.get('model')
            modules_dict[unique_id] = module

        return modules_dict
