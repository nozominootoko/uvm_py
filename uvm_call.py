from uvm_sv import  uvm_sv
FUNCTION = "function"
TASK = "task"
class uvm_call(uvm_sv):
    
    def __init__(self, name:str, parent:uvm_sv = None):
        super().__init__()
        self.name = name
        self.parent = parent
        self.call_type = "void" #调用类型，function或task
        
        self.return_type = None #返回值类型，仅当call_type为function时有效,如果是task则为None
        self.extern = False #是否是extern函数
        self.extern_gen = False #是否生成extern函数
        
        if parent is not None:
            parent.add_call(self)
        self.cont_function = self.default_cont_func #生成代码的函数，默认为default_cont_func，可以根据需要修改为其他函数
        
    def default_cont_func(self):
        cont = ''
        for code in self._uvm_codes:
            cont+=code.gen_code()
            cont+=""
        
        return cont
    
    def set_content_function(self, content_function):
        self.content_function = content_function
        return self
    def set_gen_code(self, gen_code:bool = True):
        self.gen_codes = gen_code
        return self
         
    def set_extern(self, extern:bool):
        self.extern = extern
        return self  
    def set_extern_gen(self, extern_gen:bool):
        self.extern_gen = extern_gen
        return self
        
    def get_return_type_string(self):
        from uvm_properties import uvm_parameter

        if self.return_type is None:
            return ""
        elif isinstance(self.return_type, uvm_sv):
            sharp_s = ''
            if len(self.return_type._sharp)>0:
                l = []
                for name,item in self.return_type._sharp.items():
                    if isinstance(item,uvm_parameter):
                        l.append(item.name)
                    elif isinstance(item,str):
                        l.append(item)
                    else:
                        l.append(name)
                sharp_s ="#("+','.join(l)+')'
            return self.return_type.get_name()+sharp_s
        else:
            return self.return_type

class uvm_function(uvm_call):
    
    def __init__(self, name:str, parent:uvm_sv):
        super().__init__(name, parent)
        self.call_type = FUNCTION
        self.return_type = "void" #默认返回值类型为void，可以根据需要修改为其他类型
    def set_return_type(self, return_type):
        self.return_type = return_type
        return self     
class uvm_task(uvm_call):
    def __init__(self, name:str, parent:uvm_sv):
        super().__init__(name, parent)
        self.call_type = TASK      