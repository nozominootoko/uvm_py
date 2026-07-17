from uvm_py import *

ura = uvm_reg_adapter("my_adapter")

ogenor = reg_generator()
ogenor.generate(ura)