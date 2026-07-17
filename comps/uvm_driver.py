from base.uvm_object import uvm_object
from base.uvm_component import uvm_component
from seq.uvm_sequence_item import uvm_sequence_item
from tlm1.uvm_analysis_port import uvm_analysis_port
from tlm1.uvm_sqr_connections import uvm_seq_item_pull_port


class uvm_driver(uvm_component):
    def __init__(self, name="uvm_driver",parent:uvm_component=None):
        super().__init__(name, parent)
        self.seq_item_port =uvm_seq_item_pull_port("seq_item_port", self).set_gen_name_code(False).set_gen_build_code(False)
        self.seq_item_prod_if=self.seq_item_port
        self.rsp_port=uvm_analysis_port("rsp_port", self).set_gen_name_code(False).set_gen_build_code(False)
        self.req:uvm_sequence_item = None
        self.rsp:uvm_sequence_item = None
        self.sharp_parameter= None
        
    type_name = "uvm_driver"
