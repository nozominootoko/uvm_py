from uvm_py import *

path = r"cnn\cnn_conv_top.sv"
dut = uvm_dut(path)
inf = auto_if(dut)

tb = tb_top_module(dut,inf)


cnn_tr = axi_tr("cnn_tr").add_lite().add_stream()
cnn_seq = uvm_sequence("cnn_seq").ex_sharp(cnn_tr)
tr = cnn_tr("tr",cnn_seq)
cnn_seq.add_child(tr)

cnn_dri = uvm_driver("cnn_dri").ex_sharp(cnn_tr)
cnn_dri.add_call(uvm_task("drive_tr",cnn_dri).add_args(cnn_tr,"tr"))
inf.config_db_get(cnn_dri.build_phase)
cnn_mon = uvm_monitor("cnn_mon")
inf.config_db_get(cnn_mon.build_phase)
cnn_agt = uvm_agent("cnn_agt")

cnn_env = uvm_env("cnn_env")
tst = uvm_test("base_test")

env = cnn_env("env",tst)
agt = cnn_agt("agt",cnn_env)
seqer = uvm_sequencer("seqer",cnn_agt).sharp(cnn_tr).set_gen_file(False)
dri = cnn_dri("dri",cnn_agt)
mon = cnn_mon("mon",cnn_agt)
dri.seq_item_port.connect(seqer.seq_item_export)

reg_start = uvm_reg("reg_start",1,True)
reg_data = uvm_reg_field("reg_data")
reg_data.configure(reg_start,1,0,"RW",1,0,1,0,0)
reg_img = uvm_reg("reg_img",8,True)
reg_data.configure(reg_img,8,0,"RW",1,0,1,0,0)
reg_weight = uvm_reg("reg_weight",72)
reg_weight0 = uvm_reg_field("reg_weight0")
reg_weight1 = uvm_reg_field("reg_weight1")
reg_weight2 = uvm_reg_field("reg_weight2")
reg_weight0.configure(reg_weight,32,0,"RW",1,0,1,0,0)
reg_weight1.configure(reg_weight,32,32,"RW",1,0,1,0,0)
reg_weight2.configure(reg_weight,8,64,"RW",1,0,1,0,0)

reg_model = uvm_reg_block("reg_model")
reg_s = reg_start("reg_s",reg_model,"8'h00")
reg_img_w = reg_img("reg_img_w",reg_model,"8'h04")
reg_img_h= reg_img("reg_img_h",reg_model,"8'h08")
reg_wei = reg_weight("reg_weight",reg_model,"8'h10")

reg_ad=uvm_reg_adapter("reg_adapter")









all_pkg =uvm_package("all_pkg")



grl_genor = general_generator()
grl_genor.generate()