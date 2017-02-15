from abc import ABCMeta
from cloudshell.shell.core.driver_context import AutoLoadResource, AutoLoadAttribute
from cloudshell.tg.ixia.breaking_point.autoload.model.structure_node import StructureNode


class Attribute(AutoLoadAttribute):
    def __init__(self, relative_address, attribute_name, attribute_value):
        self.attribute_name = attribute_name
        self.attribute_value = attribute_value
        self._relative_address = relative_address

    @property
    def relative_address(self):
        return self._relative_address.value


class Resource(AutoLoadResource, StructureNode):
    MODEL = 'Generic resource'
    NAME_TEMPLATE = 'Resource {}'
    PREFIX = 'R'

    __metaclass__ = ABCMeta

    def __init__(self, resource_id, unique_identifier):
        StructureNode.__init__(self, resource_id)
        self._unique_identifier = unique_identifier
        self._attributes = {}

    @property
    def attributes(self):
        return self._attributes.values()

    @property
    def _prefix(self):
        return self.PREFIX

    @property
    def model(self):
        return self.MODEL

    @property
    def name(self):
        return self.NAME_TEMPLATE.format(self._relative_address.path_id)

    @property
    def unique_identifier(self):
        return self._unique_identifier

    def _add_attribute(self, name, value):
        attribute = Attribute(self._relative_address, name, value)
        self._attributes[name] = attribute

    def _get_attribute(self, name):
        return self._attributes[name].attribute_value
