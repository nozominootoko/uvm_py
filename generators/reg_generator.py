
from generators.generator_deco import generator_regi
from generators.object_generateor import object_generator

@generator_regi(name="reg_genor")
class reg_generator(object_generator):
    
    def __init__(self):
        super().__init__()

class reg_block_generator(object_generator):
    
    def __init__(self):
        super().__init__()