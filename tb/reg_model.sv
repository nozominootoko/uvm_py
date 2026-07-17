

class reg_model extends uvm_reg_block;

	reg_start                     		reg_s;
	reg_img                       		reg_img_w;
	reg_img                       		reg_img_h;
	reg_weight                    		reg_weight;
	`uvm_object_utils(reg_model)



	function new (string name = "reg_model");
		super.new(name,UVM_COVERAGE);
	endfunction 

	virtual function void build ();

		reg_s        = reg_start::type_id::create("reg_s",,get_full_name());
		reg_img_w    = reg_img::type_id::create("reg_img_w",,get_full_name());
		reg_img_h    = reg_img::type_id::create("reg_img_h",,get_full_name());
		reg_weight   = reg_weight::type_id::create("reg_weight",,get_full_name());

		reg_s.configure(this);
		reg_img_w.configure(this);
		reg_img_h.configure(this);
		reg_weight.configure(this);

		reg_s.build();
		reg_img_w.build();
		reg_img_h.build();
		reg_weight.build();

		default_map = create_map("default_map", 'h0, 4, UVM_LITTLE_ENDIAN, 1);
		default_map.add_reg(reg_s       ,8'h00,"RW");
		default_map.add_reg(reg_img_w   ,8'h04,"RW");
		default_map.add_reg(reg_img_h   ,8'h08,"RW");
		default_map.add_reg(reg_weight  ,8'h10,"RW");


	endfunction 


endclass: reg_model

