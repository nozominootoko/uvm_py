from base.uvm_component import uvm_component


class uvm_monitor(uvm_component):
    type_name = "uvm_monitor"
    
    def __init__(self, name="uvm_monitor", parent:uvm_component=None):
        super().__init__(name, parent)
