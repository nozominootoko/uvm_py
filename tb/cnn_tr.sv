

class cnn_tr extends uvm_sequence_item;

//

	logic [8:0]                   		s_axil_awaddr;
	logic                         		s_axil_awvalid;
	logic                         		s_axil_awready;
//

	logic [32:0]                  		s_axil_wdata;
	logic [4:0]                   		s_axil_wstrb;
	logic                         		s_axil_wvalid;
	logic                         		s_axil_wready;
//

	logic [2:0]                   		s_axil_bresp;
	logic                         		s_axil_bvalid;
	logic                         		s_axil_bready;
//

	logic [8:0]                   		s_axil_araddr;
	logic                         		s_axil_arvalid;
	logic                         		s_axil_arready;
//

	logic [32:0]                  		s_axil_rdata;
	logic [2:0]                   		s_axil_rresp;
	logic                         		s_axil_rvalid;
	logic                         		s_axil_rready;
	logic [32:0]                  		s_axis_tdata;
	logic                         		s_axis_tvalid;
	logic                         		s_axis_tready;
//

	logic [32:0]                  		m_axis_tdata;
	logic                         		m_axis_tvalid;
	logic                         		m_axis_tready;
	`uvm_object_utils(cnn_tr)



	function new (string name = "cnn_tr");
		super.new(name);
	endfunction 


endclass: cnn_tr

