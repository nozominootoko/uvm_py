from base.uvm_object import uvm_object
from uvm_call import uvm_function, uvm_task
from uvm_codes import build_code, connect_code, super_new_code



class uvm_component(uvm_object):
    
    def __init__(self, name, parent = None):
        super().__init__(name, parent)
        self.new_function = uvm_function("new", self).set_gen_code(True).add_args("string", "name").add_args("uvm_component", "parent", "null")
        self.new_function.add_code(super_new_code(self,self.new_function))
        self.new_function.return_type = ""
        
        self.build_phase = self.get_default_call("build_phase", "f").set_gen_code(True).set_virtual(False).set_extern(False)
        self.build_phase.add_code(build_code(self,self.build_phase))
        
        self.connect_phase = self.get_default_call("connect_phase", "f").set_gen_code(False).set_virtual(False).set_extern(False)
        self.add_code(connect_code(self,self.connect_phase))
        
        self.end_of_elaboration_phase = self.get_default_call("end_of_elaboration_phase", "f")
        self.start_of_simulation_phase = self.get_default_call("start_of_simulation_phase", "f")
        self.run_phase = self.get_default_call("run_phase", "t")
        self.pre_reset_phase = self.get_default_call("pre_reset_phase", "t")
        self.reset_phase = self.get_default_call("reset_phase", "t")
        self.post_reset_phase = self.get_default_call("post_reset_phase", "t")
        self.pre_configure_phase = self.get_default_call("pre_configure_phase", "t")
        self.configure_phase = self.get_default_call("configure_phase", "t")
        self.post_configure_phase = self.get_default_call("post_configure_phase", "t")
        self.pre_main_phase = self.get_default_call("pre_main_phase", "t")
        self.main_phase = self.get_default_call("main_phase", "t")
        self.post_main_phase = self.get_default_call("post_main_phase", "t")
        self.pre_shutdown_phase = self.get_default_call("pre_shutdown_phase", "t")
        self.shutdown_phase = self.get_default_call("shutdown_phase", "t")
        self.post_shutdown_phase = self.get_default_call("post_shutdown_phase", "t")
        self.extract_phase = self.get_default_call("extract_phase", "f")
        self.check_phase = self.get_default_call("check_phase", "f")
        self.report_phase = self.get_default_call("report_phase", "f")
        self.final_phase = self.get_default_call("final_phase", "f")
        self.phase_started = self.get_default_call("phase_started", "f")
        self.phase_ready_to_end = self.get_default_call("phase_ready_to_end", "f")
        self.phase_ended = self.get_default_call("phase_ended", "f")
        self.gen_file = True
        
        self.has_parent = True
        
    def get_default_call(self,name:str, call_type:str) -> uvm_function | uvm_task:
        if call_type == "f":
            return uvm_function(name, self).set_gen_code(False).set_return_type("void").set_virtual(True).set_extern(True).set_extern_gen(False).add_args("uvm_phase", "phase")
        if call_type == "t":
            return uvm_task(name, self).set_gen_code(False).set_virtual(True).set_extern(True).set_extern_gen(False).add_args("uvm_phase", "phase")   

    
    def get_genor_type(self):
        return "comp_genor"    
    
    def get_uu(self):
        return "component"

