

class reg_start extends uvm_reg;

	uvm_reg_field                 		reg_data;
	`uvm_object_utils(reg_start)



	function new (string name = "reg_start");
		super.new(name,1,UVM_COVERAGE);
	endfunction 

	virtual function void build ();
		reg_data = uvm_reg_field::type_id::create("reg_data");

		reg_data.configure(this, 8, 0,  "RW", 1, 0, 1, 0, 0);


	endfunction 


endclass: reg_start

