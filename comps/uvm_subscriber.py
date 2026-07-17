from typing import override
from base.uvm_component import uvm_component
from tlm1.uvm_analysis_port import uvm_analysis_imp


class uvm_subscriber(uvm_component):
    
    def __init__(self, name: str, parent: 'uvm_component'= None):
        super().__init__(name, parent)
        self.analysis_export = uvm_analysis_imp("analysis_imp",self).set_gen_build_code(False).set_gen_name_code(False).set_gen_new(False)  # Placeholder for analysis export


    
    @override
    def write(self, t):
        pass  # To be implemented in derived classes