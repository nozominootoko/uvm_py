from base_genor import construct_genor
from generators.generator_deco import generator_regi

from uvm_sv import  uvm_sv

@generator_regi(name="obj_genor")
class object_generator(construct_genor):
    
    def __init__(self):
        super().__init__()
        self.uvm_utils_str = "object"
        
    def uvm_utils(self):
        from uvm_properties import uvm_parameter
        cont = ''
        tp = self.uvm_utils_str
        child_objs = self.obj.get_children()
        
        child_list = []
        for child in child_objs:
            if child.is_uu:
                child_list.append(child)
        para = ""
        sharp_s = ''
        if len(self.obj._sharp)>0:
            para = "_param"
            l = []
            for name,item in self.obj._sharp.items():
                if isinstance(item,uvm_parameter):
                    l.append(item.name)
                elif isinstance(item,str):
                    l.append(item)
                else:
                    l.append(name)
            sharp_s ="#("+','.join(l)+')'
        if len(child_list) == 0:
            cont += f"\t`uvm_{tp}{para}_utils({self.obj.get_name()}{sharp_s})\n\n"
            return cont 
        
        utils_begin_str = f"\t`uvm_{tp}_utils_begin({self.obj.get_name()}{sharp_s})\n"
        utils_end_str = f"\n\t`uvm_{tp}_utils_end\n\n"
        uvm_field_objects =[]
    
        cont += utils_begin_str
        for child in child_list:
            quen_pre = ""
            if child.get_count_str():
                quen_pre ="_queue"
            uvm_field_objects.append(f"\t\t`uvm_field{quen_pre}_{child.get_uu()}({child.get_name():<10},UVM_ALL_ON)")
            
        utils_str = "\n".join(uvm_field_objects)
        cont += utils_str
        cont += utils_end_str
        return cont