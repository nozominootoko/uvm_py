from base.uvm_component import uvm_component


class uvm_scoreboard(uvm_component):
    type_name = "uvm_scoreboard"
    
    def __init__(self, name="uvm_scoreboard", parent:uvm_component=None):
        super().__init__(name, parent)
        
