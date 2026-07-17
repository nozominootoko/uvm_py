from typing import TYPE_CHECKING

from base.uvm_transaction import uvm_transaction

if TYPE_CHECKING:
    from seq.uvm_sequencer_base import uvm_sequencer_base


class uvm_sequence_item(uvm_transaction):
    
    issued1,issued2=None,None
    print_sequence_info = True
    def __init__(self, name="uvm_sequence_item"):
        super().__init__(name)
        self.m_sequence_id = -1
        self.m_use_sequence_info: bool 
        self.m_depth = -1
        self.m_sequencer: 'uvm_sequencer_base' = None
        self.m_parent_sequence = None
        self.gen_file=True
        
    
    def set_sequence_id(self, id: int):
        self.m_sequence_id = id  
         
    def get_sequence_id(self) -> int:
        return self.m_sequence_id
    
    def set_use_sequence_info(self, value: bool):
        self.m_use_sequence_info = value
        
    def get_use_sequence_info(self) -> bool:
        return self.m_use_sequence_info
    
    def set_id_info(self,item: 'uvm_sequence_item'):
        if item is not None:
            self.set_sequence_id(item.get_sequence_id())
            self.set_transaction_id(item.get_transaction_id())
        else:
            raise Exception("Item is None")
        
    def set_sequencer(self, sequencer):
        self.m_sequencer = sequencer