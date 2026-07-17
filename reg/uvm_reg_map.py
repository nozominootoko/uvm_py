from base.uvm_object import uvm_object


class uvm_reg_map_info:
    
    def __init__(self):
        self.offset = 0
        self.rights:str
        self.unmapped:bool 
        self.addr = list()
        self.frontdoor
        self.mem_range
        self.is_initialized:bool 
        
class uvm_reg_map(uvm_object):
    type_name = "uvm_reg_map"
    
    def __init__(self, name: str = "default_map"):
        super().__init__(name)
        self.m_base_addr 
        self.m_n_bytes: int
        self.m_endian
        self.m_byte_addressing: bool
        self.m_sequence_wrapper
        self.m_adapter
        self.m_sequencer
        self.m_auto_predict: bool = False
        self.m_check_on_read : bool = False
        
        self.m_parent
        
        self.m_system_n_bytes
        
        self.m_parent_map: uvm_reg_map 
        self.m_parent_maps: list[uvm_reg_map] = list()
        self.m_submaps: list[uvm_reg_map] = list()
        self.m_submap_rights: list[uvm_reg_map] = list()
        
        self.m_regs_by_offset:list
        self.m_regs_by_offset_wo:list
        self.m_mems_by_offset:list
        
        self.m_backdoor
        
    def configure(self,parent,base_addr,n_bytes,endian,byte_addressing = True):
        self.m_parent = parent
        self.m_base_addr = base_addr
        self.m_n_bytes = n_bytes
        self.m_endian = endian
        self.m_byte_addressing = byte_addressing
        
    def add_reg(self,rg,offset,rights = "RW",unmapped = False,frontdoor = None):
        pass
    
    def add_mem(self,mem,offset,rights = "RW",unmapped = False,frontdoor = None):
        pass
    
    def add_submap(self,child_map,offset):
        pass
    
    def add_parent_map(self,parent_map:'uvm_reg_map',offset):
        self.m_parent_map = parent_map
        self.m_parent_maps[parent_map] = offset
        parent_map.m_submaps[self] = offset 
    
    def set_sequencer(self,sequencer,adapter = None):
        self.m_sequencer = sequencer
        self.m_adapter = adapter
        
    def get_parent(self):
        return self.m_parent
    
    def get_parent_map(self):
        return self.m_parent_map
    
    def get_root_map(self):
        curr_map = self
        while curr_map.m_parent_map is not None:
            curr_map = curr_map.m_parent_map
        return curr_map
    
    def get_full_name(self):
        get_full_name = self.get_name()
        if self.m_parent is  None:
            return get_full_name
        else:
            return self.m_parent.get_full_name() + "." + get_full_name
