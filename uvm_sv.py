
from port_connection import port_connection
from pub_obj import add_obj


class uvm_sv:
    def __init__(self):
        self.name = ""#这个对象的名字
        self.parent = None #包含这个对象的类
        self.value = None #这个对象的值
        self.annotation = [] #这个对象的注释
        self.class_name = self.__class__.__name__ #这个对象的类名
        
        self.calls = {}#这个对象包含的函数，key为函数名，value为参数列表
        self.properties = {}#这个对象包含的属性，key为属性名，value为属性值
        self.kids = {}#这个对象包含的子对象
        self.args_types = {} #调用这个function或task的参数类型列表
        self._sharp = {}
        self._ex_sharp = {}
        self.constraints={}
        self.codes_dict:dict[str,uvm_code] = {}
        self.includes =[]
        self.imports = []
        
        
        self.gen_name_code = True #表示是否生成声明代码
        self.gen_build_code = True #表示是否在build_phase函数中生成实例化代码
        self.gen_new_code = True#表示是否在new函数中生成实例化代码
        self.gen_codes = True #表示是否生成代码
        self.gen_file = False
        self.has_parent = False
        
        self.arg_count =1
        self.ex_arg_count = 1
        self._count:int =1#表示这个对象的数量，默认为1
        
        self.privilege = ""#权限类别，分别为public、protected、local
        self.unsigned = False#表示是否为无符号数
        self.rand = False#表示是否为随机变量
        self.virtual = False#表示是否为虚函数
        self.pure_virtual = False#表示是否为纯虚函数
        
        self.before_class_content = []#类内容之前的代码
        self.after_class_content = []#类内容之后的代码
        
        self._uvm_codes:list[uvm_code] = []#这个对象包含的代码
        self.is_uu = False
        
        self.object_utils = "object"
        from uvm_codes import uvm_field_code
        self.uvm_field_code = uvm_field_code(self)
        self.codes_dict['uvm_field_code']=self.uvm_field_code
        
        self.prefix_leg = 40
        
        self.arg_sep = ""
    def add_include(self,include):
        
        inc = "`include"
        cont = ''
        if isinstance(include,str):
            cont = "\""+include+"\""
        elif isinstance(include,uvm_sv):
            cont="\""+include.name+".sv\""      
        else:
            raise ValueError("unsupported type") 
        s = f"{inc} {cont}"
        self.includes.append(s)     
    def add_import(self,imp):
        ims = "import"
        cont = ''
        if isinstance(imp,str):
            cont = imp
        elif isinstance(imp,uvm_sv):
            cont=imp.name     
        else:
            raise ValueError("unsupported type") 
        s = f"{ims} {cont}::*"
        self.imports.append(s)       
    def add_constraint(self,constraint):
        self.constraints[constraint.name] = constraint
        return self
        
        
    def config_db_get(self, call,vif="vif"):
        from uvm_codes import if_build_code
        from uvm_sv import uvm_interface
        #给call所属的comp加上声明
        vif = uvm_interface(vif,call.parent).set_virtual(True).set_gen_file(False)
        vif.class_name = self.name     
        call.add_code(if_build_code(vif,call,vif.name)) 
        
        return self   
        
        
    def set_gen_file(self,gen= True):
        self.gen_file = gen
        return self   
    def set_rand(self,rand:bool= True):
        self.rand = rand
        return self
            
    def get_code(self,name):
        self.codes_dict.get(name,uvm_code(self))
    def get_parent(self):
        return self.parent
                 
    def uvm_utils(self,is_uu:bool=True):
        self.is_uu = is_uu
        return self
    
    
    def add_code(self, code):
        self._uvm_codes.append(code)
        return self
    
    def add_call(self, call):
        self.calls[call.name] = call
        
    def add_child(self, child):
        self.kids[child.name] = child
        child.parent = self
    
    def add_children(self, children):
        if not isinstance(children, list):
            raise ValueError("children should be a list")
        for child in children:
            self.add_child(child)
    
    def get_children(self):
        return self.kids.values()
    
    def get_child(self,name):
        return self.kids[name]
    
    def get_num_children(self) -> int:
        return len(self.kids)
    
    def has_children(self) -> bool:
        return len(self.kids) > 0
    
    def add_property(self,p:'uvm_sv'):
        self.properties[p.name] = p

        return self
    def get_common_parent(self, other:'uvm_sv'):
        #找到相同的父节点
        all_parents = []
        other_parents = []
        parent1 = self.parent
        parent2 = other.parent
        while parent1 is not None:
            all_parents.append(parent1)
            parent1 = parent1.parent
        while parent2 is not None:
            other_parents.append(parent2)
            parent2 = parent2.parent
        for p in all_parents:
            if p in other_parents:
                return p        
        return None
        

    def get_properties(self) -> list:
        return self.properties.values()
    def get_property(self, name: str):
        return self.properties.get(name)
    
    def get_num_properties(self) -> int:
        return len(self.properties)
    
    def has_properties(self) -> bool:
        return len(self.properties) > 0
    def get_annotation(self):
        if len(self.annotation) == 0:
            return ""
        lines = []
        for item in self.annotation:
            if item is None:
                continue
            text = str(item)
            lines.append(text)
        if not lines:
            return ""
        cont_lines = []
        for text in lines:
            if text == "":
                cont_lines.append("")
            else:
                cont_lines.append("//" + text)
        return "\n".join(cont_lines) + "\n"
    def set_virtual(self, virtual:bool = True):
        self.virtual = virtual
        return self      
    
    def set_rand(self, rand: bool = True):
        self.rand = rand
        return self   
    def set_unsigned(self, unsigned: bool = True):
        self.unsigned = unsigned
        return self    
    def set_pri(self,pri:str):
        self.privilege = pri 
        return self       
    def sharp(self,*values,**kwargs):
        """Set multiple sharp entries with auto-generated names."""
        for value in values:
            name = f"default_{self.arg_count}"
            self._sharp[name] = value
            self.arg_count += 1
        for name, value in kwargs.items():
            self._sharp[name] = value
        return self
    def ex_sharp(self,*values,**kwargs):
        """Set multiple sharp entries with auto-generated names."""
        for value in values:
            name = f"default_{self.arg_count}"
            self._ex_sharp[name] = value
            self.ex_arg_count += 1
        for name, value in kwargs.items():
            self._ex_sharp[name] = value
        return self
    def get_ex_sharp(self,name:str = None):
        if name is None:
            l = []
            for name, value in self._ex_sharp.items():
                if isinstance(value, uvm_sv):
                    l.append(value.name)
                if isinstance(value, str):
                    l.append(value)
            if not l:
                return ""
            cont = ",".join(l)
            return "#(" + cont + ")"
        return str(self._sharp.get(name, "uvm_object")) 
    def get_sharp(self, name: str = None):
        """Get sharp content.

        - get_sharp() -> returns combined parameter list like "#(a,b,...)"
        - get_sharp(name) -> returns the value for the given name or 'uvm_object'
        """
        if name is None:
            l = []
            for name, value in self._sharp.items():
                if isinstance(value, uvm_sv):
                    l.append(value.name)
                elif isinstance(value, str):
                    l.append(value)
            if not l:
                return ""
            cont = ",".join(l)
            return "#(" + cont + ")"
        return self._sharp.get(name, "uvm_object")  

    def set_count(self,count = 1):
        '''
        考虑到有一个参数p
        可传入整数，如6，生成形式为p[6]
        若传入"[]"，则生成为p[]
        传入"$",则生成p[$]
        '''
        
        self._count = count
        return self
    def get_count(self):
        return self._count
    def get_count_str(self):
        if self._count ==1:
            return ""
        elif self._count == "[]":
            return "[]"
        else:
            return "["+str(self._count)+":0]"
    def clear_sharp(self):
        self._sharp.clear()
        self.arg_count = 1
    
    #重载//运算符，用来给对象添加注释，生成形式为a // b，其中a为对象名称，b为注释内容
    def __floordiv__(self, other):
        if isinstance(other, str):
            self.annotation.append(other)
            return self
        raise TypeError("Unsupported type for division: {}".format(type(other)))
    
    def get_genor_type(self):
        return "void_genor"
    
    def add_args(self,arg_type:str ,arg_name:str,default_value = None,direction:str = None):
        self.args_types[arg_name] = uvm_arg(arg_type, arg_name, default_value, direction)   
        return self  
           
    def get_args_string(self):
            args_str_list = []
            for arg_name, arg_obj in self.args_types.items():
                if isinstance(arg_obj.arg_type, uvm_sv):

                    arg_type = arg_obj.arg_type.name              
                elif isinstance(arg_obj.arg_type, str):
                                    
                    arg_type = arg_obj.arg_type
                arg_direction = arg_obj.direction
                
                if arg_direction is not None:
                    arg_type = f"{arg_direction} {arg_type:<10}"
                if arg_obj.default_value is not None:
                    args_str_list.append(f"{self.arg_sep}{arg_type} {arg_name} = {arg_obj.default_value}")
                else:
                    args_str_list.append(f"{self.arg_sep}{arg_type} {arg_name}")
            return ", ".join(args_str_list)
    
    def get_type_name(self):
        return self.class_name    
    
    def set_name(self, name: str):
        self.name = name
    
    def get_name(self) -> str:
        return self.name
    def __call__(self, name, parent):

        #当时使用这个方法时，会创建出一个新的对象，并将其父对象设置为parent
        new_obj = self.__class__(name, parent)
        self.parent = parent
        new_obj.set_gen_file(False)
        new_obj.class_name = self.name
        #会将老对象中的属性和方法复制到新对象中
        for child in self.kids.values():
            new_obj.add_child(child)    
        return new_obj
    def get_width(self):
        return ""
    def set_parent(self, parent:'uvm_sv'):
        parent.add_child(self)
        self.parent = parent
        
        return self

    def set_gen_build_code(self,gen_build_code:bool=False):
        self.gen_build_code = gen_build_code
        return self 
    
    def set_gen_name_code(self,gen_name_code:bool=False):
        self.gen_name_code = gen_name_code
        return self 
    def get_uu(self):
        return "object"
    
class uvm_arg(uvm_sv):
    def __init__(self,arg_type, name:str, default_value=None,direction:str = None):
        
        self.name = name
        self.arg_type = arg_type
        self.default_value = default_value
        self.direction = direction



#uvm_code基础代码类
class uvm_code():
    
    def __init__(self, obj:uvm_sv):
        self.content = ""
        self.tab_count = 0
        self.obj = obj #这个代码适用的对象，如function或task等
        self._uvm_codes=[]
    def set_code_obj(self, obj):
        self.obj = obj
        return self
    def before_code(self):
        
        pass
    def get_inter_code(self):
        cont=''
        for code in self._uvm_codes:
            cont += code.gen_code()   
        return cont
    def main_code(self):
        
        self.content += f""
          
    def after_code(self):
        #对齐代码，根据tab_count的值添加相应数量的制表符
        tab_str = "\t" * self.tab_count
        #划分代码行
        code_lines = self.content.split("\n")
        #给每行代码添加制表符
        code_lines = [tab_str + line if line.strip() != "" else line for line in code_lines]
        self.content = "\n".join(code_lines)
        
    #重载+运算符，使得可以直接使用+号将代码字符串添加到content中
    def __add__(self, other):
        if isinstance(other, str):
            self.content += other
            return self
        raise TypeError("Unsupported type for addition: {}".format(type(other)))
    
    def gen_code(self):
        
        if (self.obj is not None) and (not self.obj.gen_codes):
            return ""
        
        if isinstance(self.obj, list):
            return self.gen_list_code(self.obj)

        self.before_code()
        self.main_code()
        self.after_code()

        return self.content
    
    def gen_list_code(self, obj_list):
        cont = ""
        for obj in obj_list:
            self.content = ""
            self.set_code_obj(obj)
            cont += self.gen_code()
        return cont       

class uvm_construct(uvm_sv):
    def __init__(self,name, parent:uvm_sv = None):
        super().__init__()
        self.name = name
        self.parent = parent
        if parent is not None:
            parent.add_child(self)
        self.contruct_type = "construct"
        self.connect_collection: list[port_connection] = []
        self.arg_sep = "\n\t"
        
    def get_extends_str(self):
        
        return ""
    
    def add_properties(self,obj):
        if isinstance(obj,list):
            for o in obj:
                self.add_child(o)  
            return self
        self.kids[obj.get_name()] = obj  
        return self        

    

class uvm_class(uvm_construct):
    def __init__(self, name, parent:uvm_sv = None):
        super().__init__(name, parent)
        self.contruct_type = "class"

class uvm_module(uvm_construct):
    def __init__(self, name, parent:uvm_sv = None):
        super().__init__(name, parent)
        self.contruct_type = "module"
        add_obj(self)
        
        
class uvm_interface(uvm_construct):
    def __init__(self,name = None, parent:uvm_sv = None):
        super().__init__(name, parent)

        self.clocking_list = []
        self.modport_list = []
        self.left_timescale = None
        self.right_timescale = None
        self.contruct_type = "interface"
        self.gen_file = True
        add_obj(self)
        
    def add_clocking(self, clocking):
        self.clocking_list.append(clocking)
        return self
    def add_modport(self, modport):
        self.modport_list.append(modport)
        return self
    def get_genor_type(self):
        return "if_genor"
    def set_timescale(self, left, right):
        self.left_timescale = left
        self.right_timescale = right
        return self
    def get_timescale_str(self):
        if self.left_timescale and self.right_timescale:
            return f"`timescale {self.left_timescale}/{self.right_timescale}\n\n"
        return ""
    def sharp(self,**values):
        
        for name, value in values.items():
            self._sharp[name] = value
        return self
    
    def get_sharp(self, name: str = None):
        cont = ''
        con_l = []
        if len(self._sharp) == 0:
            return ""
         
        for key, value in self._sharp.items():
            con_l.append(f"\tparameter {key} = {value.value}")
        cont += ",\n".join(con_l)
        cont = "#(\n" + cont + "\n)"
        return cont
    
class uvm_package(uvm_construct):
    
    def __init__(self, name):
        super().__init__(name, None)
        self.contruct_type = "package"
        self.gen_file = True
        self.add_import("uvm_pkg")
        self.add_include("uvm_macros.svh")
        add_obj(self)
    def get_genor_type(self):
        return "pac_genor"
    
        

class uvm_clocking(uvm_sv):
    def __init__(self,name = None,parent_if = None):
        super().__init__()
        self.name = name
        self.parent_if = parent_if if isinstance(parent_if, uvm_interface) else None
        self.parent_if.add_clocking(self) if self.parent_if else None
        self._out_list = []
        self._in_list = []
        
    def add_to_out_list(self,*obj):
        for o in obj:
            if isinstance(o,list):
                self._out_list.extend(o)
            else:
                self._out_list.append(o)
        return self
    def add_to_in_list(self,*obj):
        for o in obj:
            if isinstance(o,list):
                self._in_list.extend(o)
            else:
                self._in_list.append(o)
        return self
    def get_genor_type(self):
        return "void_genor"
    def get_in_str(self):
        if len(self._in_list) == 0:
            return ""
        in_str = "input  "+", ".join([obj.get_name() for obj in self._in_list])
        return in_str
    def get_out_str(self):        
        if len(self._out_list) == 0:
            return ""     
        out_str = "output "+", ".join([obj.get_name() for obj in self._out_list])
        return out_str    
class uvm_modport(uvm_clocking):
    def __init__(self,name = None,parent_if = None):
        super().__init__()
        self.name = name
        self.parent_if = parent_if if isinstance(parent_if, uvm_interface) else None
        self.parent_if.add_modport(self) if self.parent_if else None
        self._out_list = []
        self._in_list = []
        self.arg_sep = ""
        
    def add_to_out_list(self,*obj):
        for o in obj:
            if isinstance(o,list):
                self._out_list.extend(o)
            else:
                self._out_list.append(o)
        return self
    def add_to_in_list(self,*obj):
        for o in obj:
            if isinstance(o,list):
                self._in_list.extend(o)
            else:
                self._in_list.append(o)
        return self
    def get_genor_type(self):
        return "void_genor"
    
    def get_in_str(self):
        if len(self._in_list) == 0:
            return ""
        in_str = "input "+",".join([obj.get_name() for obj in self._in_list])
        return in_str
    def get_out_str(self):   
        if len(self._out_list) == 0:
            return ""     
        out_str = "output "+",".join([obj.get_name() for obj in self._out_list])
        return out_str
class uvm_constraint(uvm_sv):
    
    def __init__(self,name,parent:uvm_sv):
        super().__init__()
        parent.add_constraint(self)

class uvm_param(uvm_sv):
    def __init__(self, name: str, value: str = "",type = None):
        super().__init__()
        self.name = name
        self.value = value
        self.type = type
    