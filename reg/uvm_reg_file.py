from base import uvm_pool
from base.uvm_object import uvm_object
from base.uvm_pool import uvm_object_string_pool
from base.uvm_queue import uvm_queue
from reg.uvm_reg_block import uvm_reg_block


class uvm_reg_file(uvm_object):
    def __init__(self, name: str = "", ):
        super().__init__(name)
        
        self.parent:uvm_reg_block 
        self.m_rf:uvm_reg_file
        self.default_hdl_path = "RTL"
        self.hdl_paths_pool:uvm_object_string_pool = uvm_object_string_pool("hdl_paths")
        
    def configure(self, blk_parent: uvm_reg_block, rf_parent:'uvm_reg_file',hdl_path: str):
        self.parent = blk_parent
        self.m_rf = rf_parent
        self.add_hdl_path(hdl_path)
        
    def add_hdl_path(self,path: str,kind: str="RTL"):
        
        paths:uvm_queue=self.hdl_paths_pool.get(kind)
        paths.push_back(path)
        
    def has_hdl_path(self,kind: str="")-> bool:
        if kind=="":
            if(self.m_rf is not None):
                kind=self.m_rf.get_default_hdl_path()
            else:   
                kind=self.parent.get_default_hdl_path()
        return self.hdl_paths_pool.exists(kind)
        