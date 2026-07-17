from base.uvm_object import uvm_object
from base.uvm_component import uvm_component



class uvm_transaction(uvm_object):
    def __init__(self, name="uvm_transaction", initiator: uvm_component = None):
        super().__init__(name)
        self.__initiator = initiator
        self.__m_transaction_id = -1
        
        

    def set_transaction_id(self, id: int):
        self.__m_transaction_id = id
        
    def get_transaction_id(self) -> int:
        return self.__m_transaction_id
    
    def set_initiator(self, initiator: uvm_component):
        self.__initiator = initiator
        
    def get_initiator(self) -> uvm_component:
        return self.__initiator