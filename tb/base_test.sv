

class base_test extends uvm_test;

	cnn_env                       		env;
	`uvm_component_utils(base_test)



	function new (string name, uvm_component parent = null);
		super.new(name, parent);
	endfunction 

	function void build_phase (uvm_phase phase);
		env    = cnn_env::type_id::create("env", this);
	endfunction 



endclass: base_test

