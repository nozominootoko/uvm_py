

interface cnn_conv_top_if #(
	parameter DATA_W = 8,
	parameter ACC_W = 16,
	parameter MAX_IMG_W = 128,
	parameter KERNEL_SZ = 3,
	parameter KERNEL_NUM = KERNEL_SZ * KERNEL_SZ
);

	logic                         		clk;
	logic                         		rst_n;
	logic [31:0]                  		s_axil_awaddr;
	logic                         		s_axil_awvalid;
	logic                         		s_axil_awready;
	logic [31:0]                  		s_axil_wdata;
	logic [3:0]                   		s_axil_wstrb;
	logic                         		s_axil_wvalid;
	logic                         		s_axil_wready;
	logic [1:0]                   		s_axil_bresp;
	logic                         		s_axil_bvalid;
	logic                         		s_axil_bready;
	logic [31:0]                  		s_axil_araddr;
	logic                         		s_axil_arvalid;
	logic                         		s_axil_arready;
	logic [31:0]                  		s_axil_rdata;
	logic [1:0]                   		s_axil_rresp;
	logic                         		s_axil_rvalid;
	logic                         		s_axil_rready;
	logic [DATA_W-1:0]            		s_axis_tdata;
	logic                         		s_axis_tvalid;
	logic                         		s_axis_tready;
	logic [ACC_W-1:0]             		m_axis_tdata;
	logic                         		m_axis_tvalid;
	logic                         		m_axis_tready;



	initial begin
		clk = 0;
		forever #5 clk = ~clk;
	end
	initial begin
		rst_n = 0;
		#25 rst_n = 1;
	end

endinterface: cnn_conv_top_if

