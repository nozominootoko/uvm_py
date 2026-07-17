
from typing import TYPE_CHECKING

from base.uvm_object_globals import uvm_sequence_state
from seq.uvm_sequence_item import uvm_sequence_item

if TYPE_CHECKING:
    from seq.uvm_sequencer_base import uvm_sequencer_base



class uvm_sequence_base(uvm_sequence_item):
    type_name = "uvm_sequence_base"
    def __init__(self,name="uvm_sequence"):
        super().__init__(name)
        self.m_seq_state :uvm_sequence_state = uvm_sequence_state.CREATED
        self.m_next_transaction_id = 1
        self.m_priority = -1
        self.m_tr_handle :int 
        self.m_wait_for_grant_semaphore :int = 0
        self.m_sqr_seq_ids = list()#int
        self.children_array = list()#uvm_sequence_base
        
        self.response_quenue = list()#uvm_sequence_item
        self.response_quenue_depth = 8
        self.response_quenue_error_report_disabled :bool
        self.do_not_randomize :bool 
        self.m_sequence_process= None
        self.m_use_response_handler :bool
        self.is_rel_default:bool
        self.wait_rel_default:bool
        self.starting_phase = None
        self.gen_file = True
        
    
    def is_item(self):
        return 0
    
    def get_sequence_state(self):
        return self.m_seq_state
    
    def wait_for_sequence_state(self, state_mask:int):
       pass
   
    def start(self, sequencer, parent_sequence=None,this_priority=1,call_pre_post=1):
        
        pass
    
    def pre_start():
        pass
    
    def pre_body():
        pass
        
    def pre_do(is_item:bool):
        pass
    
    def mid_do(this_item:uvm_sequence_item):
        pass
    
    def body(self):
        print("Body definition undefined")
        
    def post_do(this_item:uvm_sequence_item):
        pass
    
    def post_body():
        pass
    
    def post_start():
        pass
    
    def set_priority(self, value:int):
        self.m_priority = value
        
    def get_priority(self):
        return self.m_priority
    
    def is_relavant(self):
        self.is_rel_default = True
        return self.is_rel_default
    
    def wait_for_relavant(self):
        #event e
        self.wait_rel_default = True
        if self.is_rel_default != self.wait_rel_default:
            raise Exception("is_relevant() was implemented without defining wait_for_relevant()")
        #@e
    
    def lock(self, sequencer: 'uvm_sequencer_base'):
        if sequencer is None:
            sequencer = self.m_sequencer
        
        if sequencer is None:
            raise Exception("Null m_sequencer reference")
        
        sequencer.lock(self)
        
    def grab(self, sequencer: 'uvm_sequencer_base'):
        if sequencer is None:
            if(self.m_sequencer is None):
                raise Exception("Null m_sequencer reference")
            self.m_sequencer.grab(self)
        
        else:
            sequencer.grab(self)
            
    def unlock(self, sequencer: 'uvm_sequencer_base'):
        if sequencer is None:
            if(self.m_sequencer is None):
                raise Exception("Null m_sequencer reference")
            self.m_sequencer.unlock(self)
        
        else:
            sequencer.unlock(self)
    
    def ungrab(self, sequencer: 'uvm_sequencer_base'):
        self.unlock(sequencer)
        
    def is_blocked(self):
        return self.m_sequencer.is_blocked(self)
    
    def has_lock(self):
        return self.m_sequencer.has_lock(self)
    
    def get_genor_type(self):
        return "seq_genor"