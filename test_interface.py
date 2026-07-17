from uvm_codes import clock_code
from uvm_py import *



apb_if = uvm_interface("apb_if")
apb_if.set_timescale("1ns", "1ps")
apb_if.add_args("bit","pclk",None,"input")
apb_if.add_args("bit","rst_n",None,"input")
apb_if.add_code(clock_code(10))
paddr = uvm_wire("paddr",None,apb_if,lbs=31,mbs=0)
psel = uvm_wire("psel",None,apb_if)
penable = uvm_wire("penable",None,apb_if)
pwrite = uvm_wire("pwrite",None,apb_if)
prdata = uvm_wire("prdata",None,apb_if,lbs=31,mbs=0)
pwdata = uvm_wire("pwdata",None,apb_if,lbs=31,mbs=0)

i = [paddr,psel,penable,pwrite,prdata]

mck = uvm_clocking("mck",apb_if)
mck.add_args("posedge","pclk")
mck.add_to_out_list(i)
mck.add_to_in_list(prdata)

sck = uvm_clocking("sck",apb_if)
sck.add_args("posedge","pclk")
sck.add_to_in_list(i)
sck.add_to_out_list(prdata)
o =[paddr,psel,penable,pwrite,pwdata]

pck = uvm_clocking("pck",apb_if)
pck.add_args("posedge","pclk")
pck.add_to_in_list(o)

clk = uvm_wire("clk")

master_mp = uvm_modport("master_mp",apb_if).add_to_in_list(clk).add_args("clocking","sck")
slave_mp = uvm_modport("slave_mp",apb_if).add_args("clocking","sck")
passive_mp = uvm_modport("passive_mp",apb_if).add_args("clocking","pck")
if_genor = if_generator()
if_genor.generate(apb_if)