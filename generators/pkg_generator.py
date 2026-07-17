from base_genor import construct_genor
from generators.generator_deco import generator_regi

@generator_regi(name="pkg_genor")
class pkg_generator(construct_genor):
    def inter_content(self):
        self.add_to_content(self.generate_before_constr())       
        self.add_to_content(self.generate_constr_head()) 
        self.add_to_content(self.add_imps())
        self.add_to_content(self.add_incs())
        self.add_to_content(self.generate_children_constr())
        self.add_to_content(self.generate_other_children_constr())
        
        self.add_to_content(self.uvm_utils())
        self.add_to_content(self.add_codes_str())
        self.add_to_content(self.generate_calls())
        self.add_to_content(self.end_of_constr()) 
        self.add_to_content(self.generate_out_constr()) 