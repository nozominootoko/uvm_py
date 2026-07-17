from base.uvm_component import uvm_component


class uvm_test(uvm_component):
    
    type_name = "uvm_test"
    
    def __init__(self, name: str, parent: 'uvm_component'= None):
        super().__init__(name, parent)
        