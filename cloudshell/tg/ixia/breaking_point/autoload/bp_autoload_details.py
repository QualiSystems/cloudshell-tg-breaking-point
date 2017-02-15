class BPAutoloadDetails(object):
    def __init__(self, root_builder, chassis_builder, modules_builder, ports_builder):
        self._elements = {}

    def build_root_element(self):
        pass

    def build_chassis_elements(self):
        pass

    def build_module_elements(self):
        pass

    def build_port_elements(self):
        pass

    def discover(self):
        self._elements.update(self.build_root())
        self._elements.update(self.build_chassis())
        self._elements.update(self.build_modules())
        self._elements.update(self.build_ports())
