

class cnn_agt extends uvm_agent;

	uvm_sequencer#(cnn_tr)        		seqer;
	cnn_dri                       		dri;
	cnn_mon                       		mon;
	`uvm_component_utils(cnn_agt)



	function new (string name, uvm_component parent = null);
		super.new(name, parent);
	endfunction 

	function void build_phase (uvm_phase phase);
		seqer  = uvm_sequencer#(cnn_tr)::type_id::create("seqer", this);
		dri    = cnn_dri::type_id::create("dri", this);
		mon    = cnn_mon::type_id::create("mon", this);
	endfunction 

	function void connect_phase (uvm_phase phase);
		dri.seq_item_port.connect(seqer.seq_item_export);
	endfunction 


endclass: cnn_agt

