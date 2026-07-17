from base.uvm_component import uvm_component
from seq.uvm_sequencer_base import uvm_sequencer_base
from seq.uvm_sequence_base import uvm_sequence_base
from seq.uvm_sequence_item import uvm_sequence_item
from seq.uvm_sequencer_analysis_fifo import uvm_sequencer_analysis_fifo
from tlm1.uvm_analysis_port import uvm_analysis_export
from tlm1.uvm_tlm_fifos import uvm_tlm_fifo


class uvm_sequencer_param_base(uvm_sequencer_base):
    
    def __init__(self, name: str, parent: uvm_component = None):
        super().__init__(name, parent)
        self.m_num_last_reqs = 1
        self.num_last_items = self.m_num_last_reqs
        self.m_num_last_rsps = 1
        self.m_num_reqs_sent: int 
        self.m_num_rsps_received: int
        
        self.rsp_export = uvm_analysis_export("rsp_export", self).set_gen_build_code(False).set_gen_name_code(False)
        self.sqr_rsp_analysis_fifo = uvm_sequencer_analysis_fifo("sqr_rsp_analysis_fifo", self).set_gen_build_code(False).set_gen_name_code(False)
        self.sqr_rsp_analysis_fifo.print_enabled = 0
        self.m_req_fifo = uvm_tlm_fifo("req_fifo", self).set_gen_build_code(False).set_gen_name_code(False)  # Placeholder for request FIFO
        self.m_req_fifo.print_enabled = 0
        
    def send_request(self,sequence_ptr: uvm_sequence_base, t:uvm_sequence_item,rerandomize:bool=False):
        pass
        
        
        
        