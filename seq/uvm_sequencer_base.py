from enum import Enum, auto
from base.uvm_component import uvm_component
from base.uvm_object_globals import uvm_sequencer_arb_mode
from seq.uvm_sequence_base import uvm_sequence_base

class uvm_sequence_request:
    def __init__(self,):
        self.grant:bool
        self.sequence_id:int
        self.request_id:int
        self.item_priority:int
        self.process_id = None
        self.request :uvm_sequencer_base.seq_req_t
        self.sequence_ptr:uvm_sequence_base

class uvm_sequencer_base(uvm_component):
    class seq_req_t(Enum):
        SEQ_TYPE_REQ=auto()
        SEQ_TYPE_LOCK=auto()
        SEQ_TYPE_GRAB=auto()

    g_request_id:int 
    g_sequence_id:int=1
    g_sequencer_id = 1
    def __init__(self, name="uvm_sequencer_base", parent:'uvm_component'=None):
        super().__init__(name, parent)
        self.arb_sequence_q=list[uvm_sequence_request]
        self.arb_completed = list[bool]
        self.lock_list = list[uvm_sequence_base]
        self.reg_sequences = list[int]
        
        self.m_lock_arb_size:int
        self.m_arb_size:int
        self.m_wait_for_item_sequence_id:int
        self.m_wait_for_item_transaction_id:int
        
        self.m_arbitration:uvm_sequencer_arb_mode = uvm_sequencer_arb_mode.SEQ_ARB_FIFO
        
        self.m_sequencer_id:int = uvm_sequencer_base.g_sequencer_id+1
        self.m_lock_arb_size = -1
    
    def build_phase(self, phase):
        super().build_phase(phase)
    
    def m_lock_req(self, sequence_ptr:uvm_sequence_base, is_lock:int):
        
        pass
    
    def m_unlock_req(self, sequence_ptr:uvm_sequence_base):
        pass
    def lock(self, sequence_ptr:uvm_sequence_base):
        self.m_lock_req(sequence_ptr,1)
        pass
    
    def grab(self, sequence_ptr:uvm_sequence_base):
        self.m_lock_req(sequence_ptr,0)
        pass
    
    def unlock(self, sequence_ptr:uvm_sequence_base):
        self.m_unlock_req(sequence_ptr)
        
    def ungrab(self, sequence_ptr:uvm_sequence_base):
        self.m_unlock_req(sequence_ptr)
    
    def start_default_sequence(self, seq:uvm_sequence_base):
        pass
    
    def run_phase(self, phase):
        super().run_phase(phase)
        self.start_default_sequence()
        pass
    
    def analysis_write(self, t):
        return