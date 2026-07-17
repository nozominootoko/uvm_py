
from seq.uvm_sequence_item import uvm_sequence_item
from uvm_properties import uvm_logic


class axi_tr(uvm_sequence_item):
    """Create a transaction object that carries AXI-Lite interface signals."""

    def __init__(self, name="axi_tr", addr_width=8, data_width=32, strb_width=4, resp_width=2):
        super().__init__(name)
        self.addr_width = addr_width
        self.data_width = data_width
        self.strb_width = strb_width
        self.resp_width = resp_width
        self.class_name = "uvm_sequence_item"
        self.gen_file=True




    def _add_signal(self, name, lbs=0, mbs=0):
        return uvm_logic(name, None, self, lbs, mbs)
    
    def add_lite(self):
        self._add_signal("s_axil_awaddr", self.addr_width)//"\n"
        self._add_signal("s_axil_awvalid")
        self._add_signal("s_axil_awready")

        self._add_signal("s_axil_wdata", self.data_width)//"\n"
        self._add_signal("s_axil_wstrb", self.strb_width)
        self._add_signal("s_axil_wvalid")
        self._add_signal("s_axil_wready")

        self._add_signal("s_axil_bresp", self.resp_width)//"\n"
        self._add_signal("s_axil_bvalid")
        self._add_signal("s_axil_bready")

        self._add_signal("s_axil_araddr", self.addr_width)//"\n"
        self._add_signal("s_axil_arvalid")
        self._add_signal("s_axil_arready")

        self._add_signal("s_axil_rdata", self.data_width)//"\n"
        self._add_signal("s_axil_rresp", self.resp_width)
        self._add_signal("s_axil_rvalid")
        self._add_signal("s_axil_rready")  

        return self
    
    def add_stream(self):
        self._add_signal("s_axis_tdata",self.data_width)
        self._add_signal("s_axis_tvalid")
        self._add_signal("s_axis_tready")
        
        self._add_signal("m_axis_tdata",self.data_width)//"\n"
        self._add_signal("m_axis_tvalid")
        self._add_signal("m_axis_tready")
        return self
        