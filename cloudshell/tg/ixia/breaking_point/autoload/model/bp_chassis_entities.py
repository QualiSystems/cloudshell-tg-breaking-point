from cloudshell.tg.ixia.breaking_point.autoload.model.autoload_elements import Resource
from cloudshell.tg.ixia.breaking_point.autoload.model.parent_aware import ParentAware


class Chassis(Resource, ParentAware):
    MODEL = 'CHASSIS'
    NAME_TEMPLATE = 'Chassis {}'
    PREFIX = 'CH'

    def __init__(self, resource_id, unique_identifier, parent_id=None):
        Resource.__init__(self, resource_id, unique_identifier)
        ParentAware.__init__(self, parent_id)

    @property
    def version(self):
        return self._get_attribute('Version')

    @version.setter
    def version(self, value):
        self._add_attribute('Version', value)

    @property
    def server_description(self):
        return self._get_attribute('Server Description')

    @server_description.setter
    def server_description(self, value):
        self._add_attribute('Server Description', value)


class Module(Resource, ParentAware):
    MODEL = 'Module'
    NAME_TEMPLATE = 'Module {}'
    PREFIX = 'M'

    def __init__(self, resource_id, unique_identifier, parent_id=None):
        Resource.__init__(self, resource_id, unique_identifier)
        ParentAware.__init__(self, parent_id)

    @property
    def device_model(self):
        return self._get_attribute('Model')

    @device_model.setter
    def device_model(self, value):
        self._add_attribute('Model', value)


class Port(Resource, ParentAware):
    MODEL = 'Port'
    NAME_TEMPLATE = 'Port {}'
    PREFIX = 'P'

    def __init__(self, resource_id, unique_identifier, parent_id=None):
        Resource.__init__(self, resource_id, unique_identifier)
        ParentAware.__init__(self, parent_id)

    @property
    def logical_name(self):
        return self._get_attribute('Logical Name')

    @logical_name.setter
    def logical_name(self, value):
        self._add_attribute('Logical Name', value)
