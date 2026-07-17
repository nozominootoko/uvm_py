

class reg_weight extends uvm_reg;

	uvm_reg_field                 		reg_weight0;
	uvm_reg_field                 		reg_weight1;
	uvm_reg_field                 		reg_weight2;
	`uvm_object_utils(reg_weight)



	function new (string name = "reg_weight");
		super.new(name,72,UVM_NO_COVERAGE);
	endfunction 

	virtual function void build ();
		reg_weight0 = uvm_reg_field::type_id::create("reg_weight0");
		reg_weight1 = uvm_reg_field::type_id::create("reg_weight1");
		reg_weight2 = uvm_reg_field::type_id::create("reg_weight2");

		reg_weight0.configure(this, 32, 0,  "RW", 1, 0, 1, 0, 0);
		reg_weight1.configure(this, 32, 32,  "RW", 1, 0, 1, 0, 0);
		reg_weight2.configure(this, 8, 64,  "RW", 1, 0, 1, 0, 0);


	endfunction 


endclass: reg_weight

