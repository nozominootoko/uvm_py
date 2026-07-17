#sv
from uvm_sv import uvm_class,uvm_interface,uvm_clocking,uvm_modport,uvm_package
from uvm_call import uvm_function,uvm_task
from auto_if import auto_if
from uvm_dut import uvm_dut
#comp
from base.uvm_component import uvm_component
from comps.uvm_agent import uvm_agent
from comps.uvm_driver import uvm_driver
from comps.uvm_env import uvm_env
from comps.uvm_monitor import uvm_monitor
from comps.uvm_scoreboard import uvm_scoreboard
from comps.uvm_subscriber import uvm_subscriber
from comps.uvm_test import uvm_test
from seq.uvm_sequencer import uvm_sequencer
#property
from uvm_properties import uvm_int,uvm_class,uvm_bit,uvm_logic,uvm_string,uvm_wire,uvm_constr_pro,uvm_parameter
#
# genor
from generators.object_generateor import object_generator
from generators.component_generator import component_generator
from generators.general_generator import general_generator
from base_genor import construct_genor
from generators.if_generator import if_generator
from generators.reg_generator import reg_generator
from generators.package_generator import package_generator
from generators.sequence_generator import sequence_generator
from generators.pkg_generator import pkg_generator
#object
from seq.uvm_sequence import uvm_sequence
from seq.uvm_sequence_item import uvm_sequence_item

#port
from tlm1.uvm_analysis_port import uvm_analysis_port,uvm_analysis_imp
from tlm1.uvm_tlm_fifos import uvm_tlm_analysis_fifo
#reg
from reg.uvm_reg_adapter import uvm_reg_adapter
from reg.uvm_reg import uvm_reg
from reg.uvm_reg_block import uvm_reg_block
from reg.uvm_reg_field import uvm_reg_field

#utils
cut = "\n"

#codes
from uvm_codes import super_new_code,clock_code,rst_code

#modules
from uvm_modules import tb_top_module
from uvm_trs import axi_tr
