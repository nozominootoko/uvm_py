
import uvm_config as uc
from uvm_py import *
path = r"F:\vivado\cnn\cnn.srcs\sources_1\imports\cnn\cnn_conv_top.sv"
uc.dir_path = "tb"
inf = auto_if(path)
# inf.add_code(clock_code())
# inf.add_code(rst_code())
# #搭建平台
# #env
# env = uvm_env("env_l")
# #agent
# agent = uvm_agent("agent_l")
# agt = agent("agt",env)
# trans = uvm_sequence_item("layernorm_tr").set_gen_file(True)
# #sequencer
# sequencer = uvm_sequencer("sequencer_l",agent)
# #driver,将tr驱动给dut
# driver = uvm_driver("driver_l").ex_sharp(trans)
# driver.add_call(uvm_task("drive_tr",driver).add_args(trans,"tr"))
# driver.run_phase.set_gen_code(True).set_extern(False)
# dri = driver("dri",agent)
# inf.config_db_get(driver.build_phase)

# #monitor,用于从接口获取信息，发送给scoreboard
# monitor = uvm_monitor("monitor_l")
# inf.config_db_get(monitor.build_phase)
# mp = uvm_analysis_port("mp",monitor)
# mon = monitor("mon",agent)
# #scoreboard收集从monitor传来的信息，记录并保存
# scl = uvm_scoreboard("scoreboard_l")
# imp = uvm_analysis_imp("item_collect",scl).sharp(trans,scl)
# sc = scl("sc",env)

# mp.connect(imp)

grl_genor = general_generator()
grl_genor.generate()