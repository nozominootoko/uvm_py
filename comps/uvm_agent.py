from base.uvm_component import uvm_component
import uvm_defines as ud

class uvm_agent(uvm_component):
    def __init__(self, name: str, parent: 'uvm_component'=None):
        super().__init__(name, parent)
        self.is_active = ud.UVM_PASSIVE
    def build_phase(self, phase):
        
        pass
    
    type_name = "uvm_agent"
    
    def get_is_active(self) -> int:
        return self.is_active