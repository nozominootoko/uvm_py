from base.uvm_object import uvm_object
from uvm_sv import  uvm_sv,uvm_interface


class base_properties(uvm_sv):
    def __init__(self,name,value=None,parent:uvm_sv=None,count = 1):
        super().__init__()
        self.name = name
        self.value = value
        self.parent = parent
        if self.parent is not None:
            self.parent.add_property(self)
        self.is_uu = False #uvm_object_utils
        self.type = "default"
        self.is_active = False
        self.object_utils = None
        self._count = count
        self.lbs = 0
        self.mbs = 0

    def uvm_utils(self,uu = True):
        self.is_uu = uu
        return self
    
    def get_name(self):
        return self.name                   
    
    def get_type_name(self):
        return self.type     

    def get_uu(self):
        return self.type
    
    def get_width(self):
        if self.lbs == 0 and self.mbs == 0:
            
            return ""
        if (not self.lbs) and (not self.mbs):
            return ""
        if isinstance(self.lbs,str) or isinstance(self.mbs,str):
            return f" [{self.lbs}:{self.mbs}]"
        else:
            return f" [{self.lbs}:{self.mbs}]"

class uvm_constr_pro(base_properties):
    def __init__(self, name, value=None, parent = None, count=1,constr_name ='None'):
        super().__init__(name, value, parent, count)
        self.type = constr_name
     
class uvm_int(base_properties):
    
    def __init__(self,name,value=None,parent = None,count = 1):
        super().__init__(name,value,parent,count)
        self.type = "int"
        self.object_utils = "int"
        
class uvm_string(base_properties):
    
    def __init__(self,name,value=None,parent = None,count = 1):
        super().__init__(name,value,parent,count)
        self.type = "string"
        self.object_utils = "string"
    
class uvm_bit(base_properties):
    
    def __init__(self,name,value=None,parent = None,lbs=0,mbs=0,count=1):
        super().__init__(name,value,parent,count)
        self.type = "bit"
        self.lbs = lbs.name if isinstance(lbs,uvm_parameter) else lbs
        self.mbs = mbs.name if isinstance(mbs,uvm_parameter) else mbs
        self.object_utils = "int"
        
    
class uvm_parameter(base_properties):
    
    def __init__(self,name,value,parent = None):
        super().__init__(name,value,parent,1)   
        self.type =   "parameter"  
        self.value_type = ""
        
class uvm_logic(uvm_bit):
    
    def __init__(self,name,value=None,parent = None,lbs=0,mbs=0,count=1):
        super().__init__(name,value,parent,lbs,mbs,count)
        self.type = "logic"
        self.object_utils = "int"
class uvm_wire(uvm_bit):
    
    def __init__(self,name,value=None,parent = None,lbs=0,mbs=0,count=1):
        super().__init__(name,value,parent,lbs,mbs,count)
        self.type = "wire"
        self.object_utils = "int"

class uvm_class(base_properties):
    
    def __init__(self,name,class_name,value=None,parent = None,count=1):
        super().__init__(name,value,parent,count)
        self.type = class_name
        cont = f"typedef class {class_name};"
        self.parent.before_class_content.append(cont)
        