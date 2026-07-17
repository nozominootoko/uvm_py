`timescale 1ns / 1ps
import npu_pkg::*;
import fixed_pkg::*;
module layernorm_tb_top    
    
#(
    parameter int SRAM_DEPTH  = 4096,
    parameter int SRAM_ADDR_W = $clog2(SRAM_DEPTH)
)(
    input  wire                        clk,
    input  wire                        rst_n,

    // ---- TB SRAM0 access (data SRAM 0, 8-bit) ----
    input  wire                        tb_sram0_wr_en,
    input  wire  [SRAM_ADDR_W-1:0]    tb_sram0_wr_addr,
    input  wire  [7:0]                tb_sram0_wr_data,
    input  wire                        tb_sram0_rd_en,
    input  wire  [SRAM_ADDR_W-1:0]    tb_sram0_rd_addr,
    output wire  [7:0]                tb_sram0_rd_data,

    // ---- TB SRAM1 access (data SRAM 1, 8-bit) ----
    input  wire                        tb_sram1_wr_en,
    input  wire  [SRAM_ADDR_W-1:0]    tb_sram1_wr_addr,
    input  wire  [7:0]                tb_sram1_wr_data,
    input  wire                        tb_sram1_rd_en,
    input  wire  [SRAM_ADDR_W-1:0]    tb_sram1_rd_addr,
    output wire  [7:0]                tb_sram1_rd_data,

    // ---- LayerNorm engine command ----
    input  wire                        layernorm_cmd_valid,
    input  wire  [15:0]               layernorm_length,
    input  wire  [15:0]               layernorm_src_base,
    input  wire  [15:0]               layernorm_dst_base,
    input  wire  [15:0]               layernorm_gamma_base,
    input  wire  [15:0]               layernorm_beta_base,
    output wire                        layernorm_busy,
    output wire                        layernorm_done);

        // LayerNorm
    logic        ln_rd0_en;
    logic [15:0] ln_rd0_addr;
    logic [7:0]  ln_rd0_data;
    logic        ln_rd1_en;
    logic [15:0] ln_rd1_addr;
    logic [7:0]  ln_rd1_data;
    logic        ln_wr_en;
    logic [15:0] ln_wr_addr;
    logic [7:0]  ln_wr_data;

    logic                    s0_a_en;
    logic [SRAM_ADDR_W-1:0] s0_a_addr;
    logic [7:0]              s0_a_dout;
    logic                    s0_b_en, s0_b_we;
    logic [SRAM_ADDR_W-1:0] s0_b_addr;
    logic [7:0]              s0_b_din;
    logic [7:0]              s1_a_dout;

    always_comb begin   
            s0_a_en   = ln_rd0_en;
            s0_a_addr = ln_rd0_addr[SRAM_ADDR_W-1:0];
            s0_b_en   = ln_wr_en;
            s0_b_we   = ln_wr_en;
            s0_b_addr = ln_wr_addr[SRAM_ADDR_W-1:0];
            s0_b_din  = ln_wr_data;   
    end

    layernorm_engine u_layernorm (
        .clk           (clk),
        .rst_n         (rst_n),
        .cmd_valid     (layernorm_cmd_valid),
        .cmd_ready     (),
        .length        (layernorm_length),
        .src_base      (layernorm_src_base),
        .dst_base      (layernorm_dst_base),
        .gamma_base    (layernorm_gamma_base),
        .beta_base     (layernorm_beta_base),
        .sram_rd0_en   (ln_rd0_en),
        .sram_rd0_addr (ln_rd0_addr),
        .sram_rd0_data (ln_rd0_data),
        .sram_rd1_en   (ln_rd1_en),
        .sram_rd1_addr (ln_rd1_addr),
        .sram_rd1_data (ln_rd1_data),
        .sram_wr_en    (ln_wr_en),
        .sram_wr_addr  (ln_wr_addr),
        .sram_wr_data  (ln_wr_data),
        .busy          (layernorm_busy_i),
        .done          (layernorm_done_i)
    );

    sram_dp #(.DEPTH(SRAM_DEPTH), .WIDTH(8)) u_sram0 (
        .clk    (clk),
        .en_a   (s0_a_en),
        .we_a   (1'b0),
        .addr_a (s0_a_addr),
        .din_a  (8'd0),
        .dout_a (s0_a_dout),
        .en_b   (s0_b_en),
        .we_b   (s0_b_we),
        .addr_b (s0_b_addr),
        .din_b  (s0_b_din),
        .dout_b ()
    );

        sram_dp #(.DEPTH(SRAM_DEPTH), .WIDTH(8)) u_sram1 (
        .clk    (clk),
        .en_a   (s1_a_en),
        .we_a   (1'b0),
        .addr_a (s1_a_addr),
        .din_a  (8'd0),
        .dout_a (s1_a_dout),
        .en_b   (tb_sram1_wr_en),
        .we_b   (tb_sram1_wr_en),
        .addr_b (tb_sram1_wr_addr),
        .din_b  (tb_sram1_wr_data),
        .dout_b ()
    );

    assign ln_rd1_data      = s1_a_dout;

    assign ln_rd0_data      = s0_a_dout;
    assign s1_a_en          = ln_rd1_en;
    assign s1_a_addr = ln_rd1_addr[SRAM_ADDR_W-1:0];

endmodule
