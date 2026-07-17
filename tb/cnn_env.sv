

class cnn_env extends uvm_env;

	cnn_agt                       		agt;
	`uvm_component_utils(cnn_env)



	function new (string name, uvm_component parent = null);
		super.new(name, parent);
	endfunction 

	function void build_phase (uvm_phase phase);
		agt    = cnn_agt::type_id::create("agt", this);
	endfunction 



endclass: cnn_env

