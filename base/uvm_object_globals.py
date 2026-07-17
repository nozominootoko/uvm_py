#生成枚举uvm_action
from enum import Enum, auto
class uvm_action(Enum):
    UVM_NO_ACTION = 0
    UVM_LOG = 1
    UVM_DISPLAY = 2
    UVM_WARNING = 3
    UVM_ERROR = 4
    UVM_FATAL = 5
    
class uvm_port_type_e(Enum):
    UVM_PORT =9
    UVM_EXPORT =6
    UVM_IMPLEMENTATION =3
    
    
class uvm_sequence_state(Enum):
    CREATED   = 1
    PRE_START = 2
    PRE_BODY  = 4
    BODY      = 8
    POST_BODY = 16
    POST_START= 32
    ENDED     = 64
    STOPPED   = 128
    FINISHED  = 256

uvm_sequence_state_enum = uvm_sequence_state

class uvm_sequencer_arb_mode(Enum):
    SEQ_ARB_FIFO = auto()
    SEQ_ARB_WEIGHTED = auto()
    SEQ_ARB_RANDOM = auto()
    SEQ_ARB_STRICT_FIFO = auto()
    SEQ_ARB_STRICT_RANDOM = auto()
    SEQ_ARB_USER = auto()
    
SEQ_ARB_TYPE = uvm_sequencer_arb_mode
