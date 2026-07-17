from base_genor import construct_genor
from generators.generator_deco import generator_regi
from uvm_codes import clocking_code, modport_code

@generator_regi(name="if_genor")
class if_generator(construct_genor):
    
    def __init__(self):
        super().__init__()
        self.uvm_utils_str = "interface"
    def generate_other_children_constr(self):
        cont = ''
        clg_code = clocking_code(self.obj)
        cont+= clg_code.gen_code()
        
        mod_code = modport_code(self.obj)
        cont += mod_code.gen_code()
        return cont   