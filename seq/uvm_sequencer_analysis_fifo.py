from base.uvm_component import uvm_component
from seq.uvm_sequencer_base import uvm_sequencer_base
from tlm1.uvm_analysis_port import uvm_analysis_imp
from tlm1.uvm_tlm_fifos import uvm_tlm_fifo


class uvm_sequencer_analysis_fifo(uvm_tlm_fifo):
    def __init__(self, name: str, parent: uvm_component = None):
        super().__init__(name, parent)
        self.analysis_export = uvm_analysis_imp("analysis_export", self)
        self.sequencer_ptr:uvm_sequencer_base= None  # Placeholder for sequencer pointer
   
    def write(self, t):
        if self.sequencer_ptr is None:
            raise Exception("The sequencer pointer is null when attempting a write")
        self.sequencer_ptr.analysis_write(t)