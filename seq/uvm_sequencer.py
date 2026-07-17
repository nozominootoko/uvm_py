from seq.uvm_sequencer_param_base import uvm_sequencer_param_base
from tlm1.uvm_sqr_connections import uvm_seq_item_pull_imp


class uvm_sequencer(uvm_sequencer_param_base):
    
    def __init__(self, name: str, parent=None):
        super().__init__(name, parent)
        self.sequence_item_requested :bool = False
        self.get_next_item_called :bool = False
        self.seq_item_export : uvm_seq_item_pull_imp = uvm_seq_item_pull_imp("seq_item_export", self).set_gen_build_code(False).set_gen_name_code(False)
        