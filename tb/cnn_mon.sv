

class cnn_mon extends uvm_monitor;

	virtual cnn_conv_top_if       		vif;
	`uvm_component_utils(cnn_mon)



	function new (string name, uvm_component parent = null);
		super.new(name, parent);
	endfunction 

	function void build_phase (uvm_phase phase);
		if(!uvm_config_db #(virtual vif)::get(null, "*","vif", vif)) begin
			`uvm_fatal("NO_VIF", "Failed to get vif")
		end

	endfunction 



endclass: cnn_mon

