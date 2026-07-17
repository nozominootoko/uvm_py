from uvm_py import *
pac = uvm_package("axi_test_pkg")
pac.add_include("uvm_macros.svh")
pac.add_import("uvm_pkg")
add = uvm_parameter("ADDR_WIDTH",8,pac)
data = uvm_parameter("DATA_WIDTH",32,pac)
genor = package_generator()
genor.generate(pac)