from pub_obj import add_obj
from uvm_codes import super_new_code
from uvm_sv import uvm_class,uvm_sv

class uvm_void(uvm_class):
    
    def __init__(self, name, parent:uvm_sv = None):
        super().__init__(name, parent)
        self.is_active = False
    def get_full_name(self) -> str:
        if self.parent is None:
            return self.name
        return f"{self.parent.get_full_name()}.{self.name}"    
        

class uvm_object(uvm_void):

    def __init__(self, name="uvm_object",parent = None):
        from uvm_call import uvm_function

        super().__init__(name, parent)
        self.name = name
        self.new_function = uvm_function("new", self).set_gen_code(True).add_args("string", "name",f"\"{self.name}\"").set_return_type("")
        self.new_function.add_code(super_new_code(self,self.new_function))
        add_obj(self)
  
    def set_active(self, active = True):
        self.is_active = active
        return self
    
    def get_genor_type(self):
        return "obj_genor"
    
    def get_extends_str(self):
        cont = ""
        cont+= self.class_name
        return cont     

    def get_sharp(self, name: str = None):
        from uvm_properties import uvm_parameter

        cont = ''
        cont_l = []
        for name,item in self._sharp.items():
            if isinstance(item,uvm_parameter):
                s = f"parameter {item.name} = {item.value}"
                cont_l.append(s)
            if isinstance(item,str):
                cont_l.append(item)
            if isinstance(item, uvm_sv):
                cont_l.append(item.name)
        cont = ','.join(cont_l)
        if cont:
            cont = f"#({cont})"
        return cont
         