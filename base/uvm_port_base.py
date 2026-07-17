from typing import override
from base import uvm_object
from base.uvm_component import uvm_component
from base.uvm_object_globals import uvm_port_type_e
from uvm_codes import connection_code, port_new_code
UVM_UNBOUNDED_CONNECTIONS = -1
s_connection_error_id = "Connection Error"
s_connection_warning_id = "Connection Warning"
s_spaces = "                       "
uvm_port_list={}
  
class uvm_port_base(uvm_object.uvm_void):
    def __init__(self,name,parent:uvm_component,port_type:uvm_port_type_e,min_size=0,max_size=0):
        super().__init__(name,parent)
        self.m_if_mask : int
        self.m_if : uvm_port_base = None
        self.m_def_index : int 
        self.m_provided_by : dict = {}
        self.m_provided_to : dict = {}
        self.m_port_type = port_type
        self.m_min_size : int = min_size
        self.m_max_size : int = max_size
        self.m_resolved : bool 
        self.m_imp_list : list
        self.imp_pos = ""#imp通道的后缀，用于区分不同的通道
        self.funcs = []#存储连接的函数对象   

        self.add_to_new()
    def set_gen_new(self,new):
        self.gen_new_code = False  
        return self
    def add_to_new(self):
        self.parent.new_function.add_code(port_new_code(self,self.parent.new_function))
    
    def imp_decl(self,imp_class_name:str):
        if self.m_port_type != uvm_port_type_e.UVM_IMPLEMENTATION:
            raise Exception("imp_decl can only be called on implementation ports")
        self.imp_pos = imp_class_name
        #给component添加宏
        prefix = self.get_type_name()
        self.parent.before_class_content.append(f"`{prefix}_decl({imp_class_name})")
        #修改imp中的函数的名字
        for func in self.funcs:
            func.set_name(f"{func.name}{imp_class_name}")
        return self
  
    def max_size(self) -> int:
        return self.m_max_size  
    def min_size(self) -> int:
        return self.m_min_size
    def is_unbounded(self) -> bool:
        return self.m_max_size == UVM_UNBOUNDED_CONNECTIONS      
    @override
    def get_connected_to(self):
        pass
    
    @override
    def get_provided_to(self):
        pass
    
    @override
    def is_port(self) -> bool:
        return self.m_port_type == uvm_port_type_e.UVM_PORT
    @override
    def is_export(self) -> bool:
        return self.m_port_type == uvm_port_type_e.UVM_EXPORT
    @override
    def is_imp(self) -> bool:
        return self.m_port_type == uvm_port_type_e.UVM_IMPLEMENTATION
    
    def size(self) -> int:
        return len(self.m_connected_to)
    
    def set_if(self,index=0):
        pass
    
    def m_get_if_mask(self):
        return self.m_if_mask
    
    def set_default_index(self,index:int):
        self.m_def_index = index
        
    def connect(self,provider:'uvm_port_base'):
        from port_connection import port_connection
        conn = port_connection(self,provider)
        
        self.get_parent().connect_collection.append(conn)
        
        from_port = conn.from_port
        to_port = conn.to_port
        #找到这两个接口的相同父节点
        common_parent:uvm_component = from_port.get_common_parent(to_port)
        if common_parent is None:
            raise Exception(f"Cannot find common parent for {from_port.get_full_name()} and {to_port.get_full_name()}")
        #在父节点的connect_phase函数中添加连接代码
        common_parent.connect_phase.set_gen_code(True)
        common_parent.connect_phase.add_code(connection_code(from_port,to_port,common_parent))
        
        self.m_provided_by[provider.get_full_name()] = provider
        provider.m_provided_to[self.get_full_name()] = self
        
    def debug_connected_to(self,level=0,max_level=-1):
        pass
    
    def debug_provided_to(self,level=0,max_level=-1):
        pass
    
    def resolve_bindings(self):
        pass
    
    def get_if(self,index=0) -> uvm_object.uvm_void:
        pass