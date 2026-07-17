from uvm_codes import dut_connect_code, top_if_new_code
from uvm_sv import uvm_module, uvm_package


class tb_top_module(uvm_module):
    
    def __init__(self,dut,interface):
        super().__init__("tb_top",None)
        self.add_import("uvm_pkg")
        self.add_include("uvm_macros.svh")
        self.gen_file = True
        self.add_code(top_if_new_code(interface))
        self.add_code(dut_connect_code(dut))
        
    def get_genor_type(self):
        return "construct_genor"


    