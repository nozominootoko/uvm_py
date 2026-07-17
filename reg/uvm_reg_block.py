from reg.uvm_reg_codes import reg_block_build_code, reg_block_new_code
from uvm_call import uvm_function
from base.uvm_object import uvm_object
from reg.uvm_mem import uvm_mem
from reg.uvm_reg import uvm_reg
from reg.uvm_reg_map import uvm_reg_map
from reg.uvm_reg_models import uvm_endianness_e, uvm_path_e,uvm_coverage_model_e
from reg.uvm_vregs import uvm_vreg


class uvm_reg_block(uvm_object):
    
    def __init__(self, name: str = "",has_coverage: int = uvm_coverage_model_e.UVM_NO_COVERAGE):
        super().__init__(name)
        self.parent: uvm_reg_block = None
        self.m_roots:dict[uvm_reg_block,bool] = {self:False}
        self.regs: dict[uvm_reg,int] = {}
        self.vregs: dict[uvm_reg,int] = {}
        self.mems: dict[uvm_mem,int] = {}
        self.maps: dict[uvm_reg_map,bool] = {}
        self.default_path = uvm_path_e.UVM_DEFAULT_PATH
        self.default_hdl_path = "RTL"
        self.backdoor =""
        self.root_hdl_paths: dict[str,str] = {}
        self.locked: bool = False
        self.has_coverage:int = has_coverage
        
        self.cover_on:int
        self.fname:str
        self.lineno:int
        self.id :int
        self.new_func = uvm_function("new",self).add_args("string","name",f"\"{name}\"").set_return_type("")
        self.new_func.add_code(reg_block_new_code(self,self.new_func))
        self.build_func = uvm_function("build",self).set_virtual()
        self.build_func.add_code(reg_block_build_code(self,self.build_func))
        
        self.default_map: uvm_reg_map = None
        self.gen_file = True
        
    def configure(self,parent: 'uvm_reg_block',hdl_path: str=""):
        self.parent = parent
        if parent is not None :
            self.parent.add_block(self)
        self.add_hdl_path(hdl_path)
    
    def create_map(self,name: str,base_addr: int,n_bytes: int,endian: uvm_endianness_e,byte_addressing: int = 1)-> uvm_reg_map:
        pass
    
    def check_data_width(self,width: int)-> bool:
        pass
    
    def set_default_map(self,map: uvm_reg_map):
        pass
    
    def get_default_map(self)-> uvm_reg_map:
        pass
    
    def set_parent(self,parent: 'uvm_reg_block'):
        if self is not parent:
            self.parent = parent
    
    def add_block(self,blk: 'uvm_reg_block'):
        pass
    
    def add_map(self,map: uvm_reg_map):
        pass
    
    def add_reg(self,reg: uvm_reg):
        pass
    
    def add_vreg(self,vreg: uvm_vreg):
        pass
    
    def add_mem(self,mem: uvm_mem):
        pass
    
    def lock_model(self):
        pass
    
    def is_locked(self)-> bool:
        return self.locked
    
    def get_full_name(self)-> str:
        if self.parent is None:
            return self.get_name()
        else:
            return self.parent.get_full_name() + "." + self.get_name()
    
    def get_parent(self)-> 'uvm_reg_block':
        pass
    
    def get_root_blocks(self,blks: list['uvm_reg_block']):
        for blk in self.m_roots.keys():
            blks.append(blk)
    
    def add_hdl_path(self,path: str,kind:str="RTL"):
        pass
    
    