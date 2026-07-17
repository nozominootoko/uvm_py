

class cnn_seq extends uvm_sequence#(cnn_tr);

	cnn_tr                        		tr;
	`uvm_object_utils(cnn_seq)



	function new (string name = "cnn_seq");
		super.new(name);
	endfunction 

	virtual task pre_body ();

	endtask 

	virtual task body ();

	endtask 


endclass: cnn_seq

