from base.uvm_component import uvm_component

from uvm_py import *

my_env = uvm_env("my_env",None)//"这是环境组件"
my_agent = uvm_agent("my_agent",my_env)
ap = uvm_analysis_port("ap",my_agent)
i_agt = my_agent("i_agt", my_env).uvm_utils().set_active(True)//"这是代理类"

o_agt = my_agent("o_agt",my_env).uvm_utils()
mdl = uvm_component("mdl",my_env)

scb = uvm_scoreboard("scb",my_env)
b1 = uvm_bit("b1",None,my_env).set_rand().set_unsigned().uvm_utils()
agt_scb_fifo = uvm_tlm_analysis_fifo("agt_scb_fifo",my_env).sharp("my_transaction")
agt_mdl_fifo = uvm_tlm_analysis_fifo("agt_mdl_fifo",my_env).sharp("my_transaction")
mdl_scb_fifo = uvm_tlm_analysis_fifo("mdl_scb_fifo",my_env).sharp("my_transaction")

i_agt.ap.connect(agt_mdl_fifo.analysis_export)

gener = component_generator()
gener.generate(my_env)