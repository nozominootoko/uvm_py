`include "uvm_macros.svh"

module tb_top;

	import uvm_pkg::*;

	cnn_conv_top_if vif();

	cnn_conv_top u_dut(
		.clk             (vif.clk),
		.rst_n           (vif.rst_n),
		.s_axil_awaddr   (vif.s_axil_awaddr),
		.s_axil_awvalid  (vif.s_axil_awvalid),
		.s_axil_awready  (vif.s_axil_awready),
		.s_axil_wdata    (vif.s_axil_wdata),
		.s_axil_wstrb    (vif.s_axil_wstrb),
		.s_axil_wvalid   (vif.s_axil_wvalid),
		.s_axil_wready   (vif.s_axil_wready),
		.s_axil_bresp    (vif.s_axil_bresp),
		.s_axil_bvalid   (vif.s_axil_bvalid),
		.s_axil_bready   (vif.s_axil_bready),
		.s_axil_araddr   (vif.s_axil_araddr),
		.s_axil_arvalid  (vif.s_axil_arvalid),
		.s_axil_arready  (vif.s_axil_arready),
		.s_axil_rdata    (vif.s_axil_rdata),
		.s_axil_rresp    (vif.s_axil_rresp),
		.s_axil_rvalid   (vif.s_axil_rvalid),
		.s_axil_rready   (vif.s_axil_rready),
		.s_axis_tdata    (vif.s_axis_tdata),
		.s_axis_tvalid   (vif.s_axis_tvalid),
		.s_axis_tready   (vif.s_axis_tready),
		.m_axis_tdata    (vif.m_axis_tdata),
		.m_axis_tvalid   (vif.m_axis_tvalid),
		.m_axis_tready   (vif.m_axis_tready)
	);


endmodule: tb_top

