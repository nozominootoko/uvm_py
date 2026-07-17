
from uvm_py import *
from generators.sequence_generator import sequence_generator



seq = uvm_sequence("seq").sharp("uvm_sequence_item")

b1 = uvm_bit("b1",1,seq).set_rand().set_unsigned().set_count(19).uvm_utils()


seq_gen = sequence_generator()
seq_gen.generate(seq)