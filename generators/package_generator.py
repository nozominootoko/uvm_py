from base_genor import construct_genor
from generators.generator_deco import generator_regi
from uvm_codes import imports_code, includes_code

@generator_regi(name="pac_genor")
class package_generator(construct_genor):
    
 
    
    def add_imps(self):
        c=includes_code(self.obj)
        c.tab_count =1
        ins = c.gen_code()
        i = imports_code(self.obj)
        ims = i.gen_code()
        ims+='\n'
        return ims + ins+"\n"
    
    def add_incs(self):
        
        return ""
        