
from generators.generator_deco import generator_regi
from generators.object_generateor import object_generator

@generator_regi(name="seq_genor")
class sequence_generator(object_generator):
    def __init__(self):
        super().__init__()
        self.out_class_content = "" #生成的外部类内容
        self.obj = None
       

    
    