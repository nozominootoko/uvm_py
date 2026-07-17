module cnn_conv_top #(
    parameter DATA_W     = 8,    // 像素/权重位宽
    parameter ACC_W      = 16,   // 累加输出位宽
    parameter MAX_IMG_W  = 128,  // 最大图像宽度
    parameter KERNEL_SZ  = 3,
    parameter KERNEL_NUM = KERNEL_SZ * KERNEL_SZ
)(
    input  logic                        clk,
    input  logic                        rst_n,

    // AXI4-Lite 配置寄存器
    input  logic [31:0]                 s_axil_awaddr,
    input  logic                        s_axil_awvalid,
    output logic                        s_axil_awready,
    input  logic [31:0]                 s_axil_wdata,
    input  logic [3:0]                  s_axil_wstrb,
    input  logic                        s_axil_wvalid,
    output logic                        s_axil_wready,
    output logic [1:0]                  s_axil_bresp,
    output logic                        s_axil_bvalid,
    input  logic                        s_axil_bready,

    input  logic [31:0]                 s_axil_araddr,
    input  logic                        s_axil_arvalid,
    output logic                        s_axil_arready,
    output logic [31:0]                 s_axil_rdata,
    output logic [1:0]                  s_axil_rresp,
    output logic                        s_axil_rvalid,
    input  logic                        s_axil_rready,

    // AXI4-Stream 图像输入
    input  logic [DATA_W-1:0]           s_axis_tdata,
    input  logic                        s_axis_tvalid,
    output logic                        s_axis_tready,

    // AXI4-Stream 卷积输出
    output logic [ACC_W-1:0]            m_axis_tdata,
    output logic                        m_axis_tvalid,
    input  logic                        m_axis_tready
);

// 内部互联信号
logic                    cfg_start;
logic [7:0]              cfg_img_w;
logic [7:0]              cfg_img_h;
logic [71:0]             cfg_weight;

logic [DATA_W*KERNEL_NUM-1:0] window_data;
logic                        window_valid;

// --------------------------
// AXI-Lite 寄存器子模块，全显式连线
// --------------------------
axil_reg u_reg_inst (
    .clk            (clk),
    .rst_n          (rst_n),
    
    .s_axil_awaddr  (s_axil_awaddr),
    .s_axil_awvalid (s_axil_awvalid),
    .s_axil_awready (s_axil_awready),
    .s_axil_wdata   (s_axil_wdata),
    .s_axil_wstrb   (s_axil_wstrb),
    .s_axil_wvalid  (s_axil_wvalid),
    .s_axil_wready  (s_axil_wready),
    .s_axil_bresp   (s_axil_bresp),
    .s_axil_bvalid  (s_axil_bvalid),
    .s_axil_bready  (s_axil_bready),

    .s_axil_araddr  (s_axil_araddr),
    .s_axil_arvalid (s_axil_arvalid),
    .s_axil_arready (s_axil_arready),
    .s_axil_rdata   (s_axil_rdata),
    .s_axil_rresp   (s_axil_rresp),
    .s_axil_rvalid  (s_axil_rvalid),
    .s_axil_rready  (s_axil_rready),

    .cfg_start      (cfg_start),
    .cfg_img_w      (cfg_img_w),
    .cfg_img_h      (cfg_img_h),
    .cfg_weight     (cfg_weight)
);

// --------------------------
// LineBuffer 滑动窗口模块，全显式连线
// --------------------------
line_buffer_3x3 #(
    .DATA_W(DATA_W),
    .MAX_W(MAX_IMG_W)
) u_line_inst (
    .clk            (clk),
    .rst_n          (rst_n),
    .cfg_start      (cfg_start),
    .cfg_img_w      (cfg_img_w),

    .s_axis_tdata   (s_axis_tdata),
    .s_axis_tvalid  (s_axis_tvalid),
    .s_axis_tready  (s_axis_tready),

    .window_data    (window_data),
    .window_valid   (window_valid)
);

// --------------------------
// MAC 3x3乘加模块，全显式连线
// --------------------------
mac_3x3 #(
    .DATA_W(DATA_W),
    .ACC_W(ACC_W)
) u_mac_inst (
    .clk            (clk),
    .rst_n          (rst_n),

    .window_data    (window_data),
    .cfg_weight     (cfg_weight),
    .window_valid   (window_valid),

    .m_axis_tdata   (m_axis_tdata),
    .m_axis_tvalid  (m_axis_tvalid),
    .m_axis_tready  (m_axis_tready)
);

endmodule