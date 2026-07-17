
from base.uvm_object import uvm_object
from uvm_call import uvm_function



class uvm_reg_adapter(uvm_object):
    
    def __init__(self, name="uvm_reg_adapter"):
        super().__init__(name)
        self.parent_sequence = None
        self.reg2bus_func = uvm_function("reg2bus",self).set_return_type("uvm_sequence_item").set_virtual().add_args("uvm_reg_bus_op", "rw",None,"ref")
        self.bus2reg_func = uvm_function("bus2reg",self).set_return_type("void").set_virtual().add_args("uvm_sequence_item", "bus_item").add_args("uvm_reg_bus_op", "rw",None,"ref")
        self.supports_byte_enable: bool = None
        self.provides_response : bool = None
        self.gen_file = True
    
    
    def set_parent_sequence(self, parent_sequence):
        self.parent_sequence = parent_sequence
        
    def get_genor_type(self):
        return "obj_genor"