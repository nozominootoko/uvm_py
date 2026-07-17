from generators.generator_deco import generator_regi
from generators.object_generateor import object_generator

@generator_regi(name="comp_genor")
class component_generator(object_generator):
    
    def __init__(self):
        super().__init__()
        self.uvm_utils_str = "component"
        
