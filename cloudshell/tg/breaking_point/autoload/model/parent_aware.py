class ParentAware(object):
    def __init__(self, parent_id):
        self._parent_id = parent_id

    @property
    def parent_id(self):
        return self._parent_id

    @parent_id.setter
    def parent_id(self, value):
        self._parent_id = value
