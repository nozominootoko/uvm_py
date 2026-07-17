from enum import Enum
class uvm_coverage_model_e(Enum):
    UVM_NO_COVERAGE     = 0
    UVM_CVR_REG_BITS    = 1
    UVM_CVR_ADDR_MAP    = 2
    UVM_CVR_FIELD_VALS  = 4
    UVM_CVR_ALL         = -1
class uvm_path_e(Enum):
    
    UVM_FRONTDOOR = 1
    UVM_BACKDOOR = 2
    UVM_PREDICT = 3
    UVM_DEFAULT_PATH = 0
    
class uvm_endianness_e(Enum):
    UVM_NO_ENDIAN = 0
    UVM_LITTLE_ENDIAN = 1
    UVM_BIG_ENDIAN = 2
    UVM_LITTLE_FIFO = 3
    UVM_BIG_FIFO = 4
    
class uvm_check_e(Enum):
    UVM_NO_CHECK = 0
    UVM_CHECK = 1
    