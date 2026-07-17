from uvm_codes import clock_code, rst_code
from uvm_dut import uvm_dut
from uvm_properties import uvm_logic
from uvm_sv import uvm_interface


class auto_if(uvm_interface):
    #这个auto_if可以根据导入的sv文件自动解析，生成对应的interface对象
    def __init__(self, path):
        super().__init__(None, None)
        self.add_code(clock_code()).add_code(rst_code())
        if isinstance(path,str):
            self.dut = uvm_dut(path)
        elif isinstance(path,uvm_dut):
            self.dut = path
        self.name = self.dut.name+"_if"
        for para in self.dut.parameters:
            self._sharp[para.name] = para
        for w in self.dut.wires:
            self.add_property(uvm_logic(w.name,None,self,w.lbs,w.mbs))    
    
        