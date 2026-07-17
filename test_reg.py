#测试reg_model相关
from uvm_py import *
reg_gen=reg_generator()
reg_gen.one_time = False

reg_IntSrc = uvm_reg("reg_IntSrc",9,False).sharp("123")
TxEmpty = uvm_reg_field("TxEmpty")
TxLow   = uvm_reg_field("TxLow")
TxFull  = uvm_reg_field("TxFull")
RxEmpty = uvm_reg_field("RxEmpty")
RxHigh = uvm_reg_field("RxHigh")
RxFull = uvm_reg_field("RxFull")
SA=uvm_reg_field("SA")

TxEmpty.configure(reg_IntSrc,1,0,"RO",1,1,1,0,0)
TxLow.configure(reg_IntSrc,1,1,"RO",1,1,1,0,0)
TxFull.configure(reg_IntSrc,1,2,"RO",1,0,1,0,0)
RxEmpty.configure(reg_IntSrc,1,4,"RO",1,1,1,0,0)
RxHigh.configure(reg_IntSrc,1,5,"RO",1,0,1,0,0)
RxFull.configure(reg_IntSrc,1,6,"RO",1,0,1,0,0)
SA.configure(reg_IntSrc,1,8,"W1C",1,0,1,0,0)

reg_gen.generate(reg_IntSrc)

reg_intMask = uvm_reg("reg_IntMask",9,False)
TxEmpty = uvm_reg_field("TxEmpty")
TxLow   = uvm_reg_field("TxLow")
TxFull  = uvm_reg_field("TxFull")
RxEmpty = uvm_reg_field("RxEmpty")
RxHigh = uvm_reg_field("RxHigh")
RxFull = uvm_reg_field("RxFull")
SA=uvm_reg_field("SA")

TxEmpty.configure(reg_intMask,1,0,"RW",0,0,1,0,0)
TxLow.configure(reg_intMask,1,1,"RW",0,0,1,0,0)
TxFull.configure(reg_intMask,1,2,"RW",0,0,1,0,0)
RxEmpty.configure(reg_intMask,1,4,"RW",0,0,1,0,0)
RxHigh.configure(reg_intMask,1,5,"RW",0,0,1,0,0)
RxFull.configure(reg_intMask,1,6,"RW",0,0,1,0,0)
SA.configure(reg_intMask,1,8,"RW",0,0,1,0,0)
reg_gen.generate(reg_intMask)

reg_TxStatus = uvm_reg("reg_TxStatus",1,False)
TxEn = uvm_reg_field("TxEn")
TxEn.configure(reg_TxStatus,1,0,"RW",0,0,1,0,0)
reg_gen.generate(reg_TxStatus)

reg_TxLWM = uvm_reg("reg_TxLWM",5,False)
TxLWM = uvm_reg_field("TxLWM")
TxLWM.configure(reg_TxLWM,5,0,"RW",0,8,1,0,0)
reg_gen.generate(reg_TxLWM)

reg_RxStatus = uvm_reg("reg_RxStatus",2,False)
RxEn = uvm_reg_field("RxEn")
RxEn.configure(reg_RxStatus,1,0,"RW",0,0,1,0,0)
AlignErr = uvm_reg_field("Align")
AlignErr.configure(reg_RxStatus,1,1,"RO",0,0,1,0,0)
reg_gen.generate(reg_RxStatus)

reg_RxHWM = uvm_reg("reg_RxHWM",5,False)
RxHWM = uvm_reg_field("RxHWM")
RxHWM.configure(reg_RxHWM,5,0,"RW",0,16,1,0,0)
reg_gen.generate(reg_RxHWM)

reg_TxRx = uvm_reg("reg_TxRx",8,False)
TxRx = uvm_reg_field("TxRx")
TxRx.configure(reg_TxRx,8,0,"RW",1,"8'h00",1,0,0)
reg_gen.generate(reg_TxRx)

reg_dut = uvm_reg_block("reg_dut",False)

IntSrc = reg_IntSrc("IntSrc",reg_dut,0)
IntMask = reg_intMask("IntMask",reg_dut,1)
TxStatus = reg_TxStatus("TxStatus",reg_dut,2)
TxLWM = reg_TxLWM("TxLWM",reg_dut,3)
RxStatus = reg_RxStatus("RxStatus",reg_dut,4)
RxHWM = reg_RxHWM("RxHWM",reg_dut,5)
TxRx = reg_TxRx("TxRx",reg_dut,6)

reg_gen.generate(reg_dut)
reg_gen.to_file("reg_model.sv")