from uvm_py import *

DW = uvm_parameter('DW',"DATA_WIDTH")
AW = uvm_parameter('AW',"ADDR_WIDTH")
axi_transaction = uvm_sequence_item("axi_transaction").sharp(DW,AW).set_gen_file()
data = uvm_logic("data",None,axi_transaction,DW).set_rand()
addr = uvm_logic("addr",None,axi_transaction,AW).set_rand()
op = uvm_constr_pro("op",None,axi_transaction,constr_name="op_code").set_rand()

random_write = uvm_function("random_write",axi_transaction)
random_read = uvm_function("random_read",axi_transaction)
set_read = uvm_function("set_read",axi_transaction)
get_copy = uvm_function("get_copy",axi_transaction).set_return_type(axi_transaction)
convert2string = uvm_function("convert2string",axi_transaction).set_return_type("string")

command_monitor = uvm_component("command_monitor",None)
ap = uvm_analysis_port("ap",command_monitor).sharp(axi_transaction)
axi_if = uvm_constr_pro("axi_if",None,command_monitor,constr_name="axi_lite_if").set_gen_file(False).config_db_get(command_monitor.build_phase).set_virtual()

driver = uvm_driver("driver",None).ex_sharp(axi_transaction)
driver.add_properties(axi_if)
axi_if.config_db_get(driver.build_phase)

scoreboard = uvm_subscriber("scoreboard",None)
res = uvm_tlm_analysis_fifo("res",scoreboard).sharp(axi_transaction).set_gen_build_code(False)
mem = uvm_logic("mem",None,scoreboard,31,count=63)
total_count = uvm_int("total_count",0,scoreboard)
success_count = uvm_int("success_count",0,scoreboard)
grl_genor = general_generator()
grl_genor.generate()