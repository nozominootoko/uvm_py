from base.uvm_object import uvm_object

from reg.uvm_reg_models import uvm_check_e, uvm_coverage_model_e


class uvm_reg_field(uvm_object):
    
    def __init__(self, name: str = "", ):
        super().__init__(name)
        from reg.uvm_reg import uvm_reg
        self.value: int =None
        self.m_mirrored:int
        self.m_desired:int
        self.m_access:str
        self.parent: uvm_reg = None
        self.m_lsb:int
        self.m_size:int
        self.m_volatile:bool
        self.m_reset:dict[str,int]={}
        self.m_written:bool
        self.m_read_in_progress:bool
        self.fname:str
        self.lineno:int
        self.m_cover_on:int
        self.m_individually_accessible:bool
        self.m_check:uvm_check_e
        
        self.m_max_size:int = 0
        self.m_policy_names:dict[str,bool]= {}
        
    def configure(self,
                  parent,
                  size: int,
                  lsb_pos: int,
                  access: str,
                  volatile: bool,
                  reset: int,
                  has_reset: bool,
                  is_rand: bool,
                  individually_accessible: bool,    ):
        '''
        函数: configure

    实例特定配置
       
        指定该字段的~parent~寄存器，字段的~size~（位宽），
        字段在寄存器中相对于寄存器最低有效位的最低有效位位置，
        字段的~access~访问策略，易失性，
        "HARD" ~reset~值，
        字段值是否实际复位
        （如果~has_reset~为FALSE，则忽略~reset~值），
        字段值是否可以随机化，
        以及该字段是否是寄存器中唯一占据一个字节通道的字段。
       
        如果字段访问策略是预定义策略且不是
        "RW", "WRC", "WRS", "WO", "W1", 或 "WO1"之一，
        则忽略~is_rand~的值，并关闭该字段实例的rand_mode()，因为它不能被写入。
        '''

        self.m_parent = parent
        parent.add_child(self)
        if size <= 0:
            raise Exception("uvm_reg_field::configure - size must be > 0")
        self.m_size = size
        self.m_volatile = volatile
        self.p_reset = reset
        self.p_has_reset= has_reset
        self.p_is_rand = is_rand
        self.p_in_acc = individually_accessible
        self.m_access = access.upper()
        self.m_lsb = lsb_pos
        self.m_cover_on = uvm_coverage_model_e.UVM_NO_COVERAGE
        self.m_written = False
        self.m_check = uvm_check_e.UVM_NO_CHECK if volatile else uvm_check_e.UVM_CHECK
        self.m_individually_accessible = individually_accessible
        
        if has_reset:
            self.set_reset(reset)
        
        self.m_parent = parent.add_field(self)
        # if self.m_access not in self.m_policy_names.keys():
        #     self.m_access = "RW"
            
        if size > self.m_max_size:
            self.m_max_size = size
            
        match self.m_access:
            case "RW" | "WR" | "RO" | "WO" | "RC" | "WC":
                is_rand =False
                import random
        # if not is_rand:
        #     self.value = random.randint(0,1024)
    def set_reset(self, value: int,kind: str="HARD"):
        # self.m_reset[kind] = value & ((1 << self.m_size) - 1)
        pass