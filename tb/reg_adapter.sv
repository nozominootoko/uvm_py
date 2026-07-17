

class reg_adapter extends uvm_reg_adapter;

	`uvm_object_utils(reg_adapter)



	function new (string name = "reg_adapter");
		super.new(name);
	endfunction 

	virtual function uvm_sequence_item reg2bus (ref uvm_reg_bus_op rw);

	endfunction 

	virtual function void bus2reg (uvm_sequence_item bus_item, ref uvm_reg_bus_op rw);

	endfunction 


endclass: reg_adapter

