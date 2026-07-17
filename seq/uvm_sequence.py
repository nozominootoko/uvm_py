from uvm_call import uvm_function, uvm_task

from seq.uvm_sequence_base import uvm_sequence_base
from uvm_codes import super_new_code


class uvm_sequence(uvm_sequence_base):
    def __init__(self, name: str):
        super().__init__(name)
        self.name = name
        self.new_func = uvm_function("new",self).add_args("string","name",f"\"{name}\"").set_return_type("")
        self.new_func.add_code(super_new_code(self,self.new_func))
        self.pre_body_func = uvm_task("pre_body",self).set_virtual(True)
        self.body_func = uvm_task("body",self).set_virtual(True)
        self.kids = {}
        
    def get_children(self) -> list:
        return self.kids.values()
    
    def get_extends_str(self):
        return self.class_name
        
        