from collections import defaultdict
from abc import ABCMeta, abstractmethod, abstractproperty


class ValidatorInterface(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def registered(self, path_id, path_prefix):
        pass

    def valid(self):
        pass


class IdValidator(ValidatorInterface):
    def __init__(self):
        self._paths = defaultdict(list)

    def registered(self, path_id, path_prefix):
        registered = False
        if path_id >= 0 and (
                    (path_id not in self._paths) or (
                                path_id in self._paths and path_prefix not in self._paths[path_id])):
            self._paths[path_id].append(path_prefix)
        else:
            registered = True
        return registered

    def get_valid(self):
        new_id = max(self._paths) + 1
        self._paths[new_id].append(None)
        return new_id


class RelativeAddress(object):
    """
    Helps to build relative address
    """

    def __init__(self, path_id, path_prefix):

        self._path_id = path_id
        self._path_prefix = path_prefix
        self._parent_resource = None

        self._valid_path_id = None
        self._duplicated = False

    @property
    def parent_resource(self):
        return self._parent_resource

    @parent_resource.setter
    def parent_resource(self, value):
        """
        :param value:
        :type value: StructureNode
        :return:
        """
        self._parent_resource = value
        if self._parent_resource.id_validator.registered(self._path_id, self._path_prefix):
            self._duplicated = True

    @property
    def valid_id(self):
        if not self._valid_path_id:
            if self._duplicated and self._parent_resource:
                self._valid_path_id = self._parent_resource.id_validator.get_valid()
            else:
                self._valid_path_id = self._path_id
        return self._valid_path_id

    @property
    def path_id(self):
        if self._path_id > 0:
            path_id = self._path_id
        else:
            path_id = self.valid_id
        return path_id

    @property
    def _local_path(self):
        if not self._path_id:
            local_path = None
        elif self._path_prefix:
            local_path = self._path_prefix + str(self.valid_id)
        else:
            local_path = str(self.valid_id)
        return local_path

    def _build_path(self):
        if self.parent_resource and self.parent_resource.relative_address:
            value = '{0}/{1}'.format(self.parent_resource.relative_address, self._local_path)
        else:
            value = self._local_path
        return value

    @property
    def value(self):
        return self._build_path()


class StructureNode(object):
    def __init__(self, resource_id):
        self._relative_address = RelativeAddress(path_id=resource_id, path_prefix=self._prefix)
        self._id_validator = None

    @abstractproperty
    def _prefix(self):
        pass

    @property
    def id_validator(self):
        if not self._id_validator:
            self._id_validator = IdValidator()
        return self._id_validator

    @property
    def relative_address(self):
        return self._relative_address.value

    def add_parent(self, resource):
        self._relative_address.parent_resource = resource
