
from __future__ import annotations

from typing import TYPE_CHECKING


from uvm_sv import uvm_code, uvm_construct, uvm_interface, uvm_sv
from uvm_call import uvm_call

if TYPE_CHECKING:
    pass


class constr_head_code(uvm_code):
    
    def __init__(self,obj:uvm_construct):
        super().__init__(obj)
        self.obj:uvm_construct = obj
        
    def main_code(self):
        cont = ""
        ctrct_type = self.obj.contruct_type
        ctrct_name = self.obj.get_name()
        extends_str = self.obj.get_extends_str()
        ex_sharp = self.obj.get_ex_sharp()
        extends_cont = ""
        if extends_str:
            extends_cont+= " extends "+extends_str+ex_sharp    
        sharp_cont = ""    
        sharp_t = self.obj.get_sharp()
        if sharp_t :
            sharp_cont +=" "+sharp_t 
        annota = self.obj.get_annotation()+"\n"
        cont += annota 
        arg_s = self.obj.get_args_string()
        arg_cont=''
        if arg_s:
            arg_cont = f"({arg_s})"
        cont += f"{ctrct_type} {ctrct_name}{sharp_cont}{arg_cont}{extends_cont};\n\n"
        self.content += cont

class declare_code(uvm_code):
    def __init__(self, obj:uvm_sv):
        super().__init__(obj)
        self.obj:uvm_construct = obj
        
    def main_code(self):
        cont = ""
        child = self.obj
        if child.gen_name_code:
                pre_fix = ""
                pri_fix = ""
                if child.privilege:
                    pri_fix = child.privilege + " "
                    pre_fix += pri_fix
                if child.rand:
                    pre_fix += "rand "
                if child.unsigned:
                    pre_fix += "unsigned " 
                if child.virtual:
                    pre_fix+= "virtual "
                type_s=child.get_type_name()+child.get_width()
                sharp_cont = ""
                sharp_t = child.get_sharp()
                if sharp_t:
                    sharp_cont += sharp_t
                count_pos = ""
                count_pos += child.get_count_str()
                value_str = ""
                if child.value is not None:
                    value_str+=f" = {str(child.value)}"
                all_pre_fix = pre_fix+type_s+sharp_cont
                anno = child.get_annotation()
                if anno:
                    cont = f"{anno}\t{all_pre_fix:<30}\t\t{child.get_name()}{count_pos}{value_str};\n"
                else:
                    cont = f"\t{all_pre_fix:<30}\t\t{child.get_name()}{count_pos}{value_str};\n"
        self.content += cont

class gen_call_code(uvm_code):
    def __init__(self, obj:uvm_call):
        super().__init__(obj)
        self.obj:uvm_call = obj
        self.out_constr_content = "" #构造函数外的内容
        self.tab_count =1

    def add_to_out_class_content(self, content):
        if self.obj.extern and self.obj.extern_gen:
            self.out_constr_content += content 
    def main_code(self):
        cont = ""
        call_type = self.obj.call_type+ " "
        call_name = self.obj.name
        rp_s = self.obj.get_return_type_string()
        return_type =  rp_s+" " if rp_s else ""
        extern_str = ""
        virtual_str = ""
        if self.obj.extern:
            extern_str = "extern "
        if self.obj.virtual:
            virtual_str = "virtual "
        privilege_str =  self.obj.privilege+" " if self.obj.privilege else ""
        
        args_str = self.obj.get_args_string()
        cont    += f"{extern_str}{virtual_str}{privilege_str}{call_type}{return_type}{call_name} ({args_str});\n"
        out_cont = f"{extern_str}{virtual_str}{privilege_str}{call_type}{return_type}{self.obj.parent.name}::{call_name} ({args_str});\n"
        self.add_to_out_class_content(out_cont)
        if not self.obj.extern:
            cont+= self.obj.cont_function()
            cont+= f"\nend{call_type}\n"
        
        if self.obj.extern and self.obj.extern_gen:
            self.add_to_out_class_content(self.obj.cont_function())
            self.add_to_out_class_content(f"\nend{call_type}\n")
        self.content+=cont
                    
class call_code(uvm_code):
    def __init__(self, obj:uvm_sv = None,call:uvm_call=None):
        super().__init__(obj)
        self.obj:uvm_sv = obj
        self.out_constr_content = "" #构造函数外的内容
        self.tab_count =1
        self.call = call

    def add_to_out_class_content(self, content):
        if self.obj.extern and self.obj.extern_gen:
            self.out_constr_content += content 
    def before_code(self):
        if isinstance(self.call,uvm_call):
            if self.call.extern:
                self.tab_count =0
    
    def main_code(self):
        cont = "//default code"
        self.content+=cont
        
class port_new_code(call_code):
    #传入的obj是一个port
    def main_code(self):         
        cont = ""
        if not self.obj.gen_name_code:
            return
        name = self.obj.name
        cont+=f"\n{name} = new(\"{name}\",this);"
        self.content+=cont

class uvm_field_code(uvm_code):
    #传入是一个uvm_sv对象，使用对象中的object_utils进行生成
    def __init__(self, obj):
        super().__init__(obj)
        self.tab_count = 2
    def main_code(self):
        cont = ''
        if self.obj.is_uu:
            cont+= f"`uvm_field_{self.obj.object_utils}({self.obj.name},UVM_ALL_ON)\n"
        
        self.content+=cont

class super_new_code(call_code):
    
    def __init__(self, obj = None,call=None):
        super().__init__(obj, call)
      
    def main_code(self):
        cont = ""
        has_parent = self.obj.has_parent
        if has_parent:
            cont += "super.new(name, parent);"
        else:
            cont += "super.new(name);"
        
        self.content+= cont

class build_code(call_code):
    #传入的是一个comp
    def main_code(self):
        from base.uvm_component import uvm_component
        cont =''
        comp:uvm_component = self.obj
        not_active_l = []
        active_l = []
        for child in comp.get_children():
            if isinstance(child,uvm_component):
                if not child.gen_build_code: 
                    continue
                sharp_s = child.get_sharp()
                s = f"{child.name:<6} = {child.class_name}{sharp_s}::type_id::create(\"{child.name}\", this);"
                if child.is_active:                   
                    active_l.append(s)
                elif not child.is_active:
                    not_active_l.append(s)
        act_s = "\n".join(active_l)
        nact_s ="\n".join(not_active_l)
        cont+= nact_s
        if active_l:
            cont+="\nif(is_active == UVM_ACTIVE) begin\n"
            cont+="\t"+act_s
            cont+="\nend"
        self.content += cont

class connect_code(call_code):
    #传入的是一个comp
    def main_code(self):
        cont =''
           
        self.content += cont
class connection_code(call_code):
    
    def __init__(self, from_port ,to_port,common_parent):
        super().__init__(None, None)
        self.from_port = from_port
        self.to_port = to_port
        self.common_parent = common_parent
    
    def main_code(self):
        cont = ''
        f_s = ""
        t_s = ""
        f_parent = self.from_port.parent
        t_parent = self.to_port.parent
        while f_parent is not None:
            if f_parent == self.common_parent:
                break
            f_s = f_parent.name + "." + f_s
            f_parent = f_parent.parent           
        while t_parent is not None:
            if t_parent == self.common_parent:
                break
            t_s = t_parent.name + "." + t_s
            t_parent = t_parent.parent
        s = f"{f_s}{self.from_port.name}.connect({t_s}{self.to_port.name});" 
        self.content+=s               
class clocking_code(uvm_code):
                   
        #传入是一个uvm_clocking对象，使用对象中的object_utils进行生成
    def __init__(self, obj: uvm_interface = None):
        super().__init__(obj)
        self.code_obj = obj
        self.tab_count = 1
        
    def main_code(self):
        cont = "\n"
        for clg in self.code_obj.clocking_list:
            
            cont += f"clocking {clg.get_name()} @({clg.get_args_string()});\n"
            out_s = clg.get_out_str()
            in_s = clg.get_in_str()
                      
            if out_s:
                if in_s:            
                    in_s=in_s+",\n"
                out_s = "\t"+out_s 
            if in_s:
                in_s = "\t"+in_s
            cont += in_s+ out_s         
            cont += "\nendclocking\n"
        self.content = cont
class modport_code(uvm_code):
    def __init__(self, obj: uvm_interface = None):
        super().__init__(obj)
        self.code_obj = obj 
        self.tab_count = 1     
    def main_code(self):
        cont = "\n"
        modport_str = ""
        for modport in self.code_obj.modport_list:
            cont += f"modport {modport.get_name()}("
            arg_s = modport.get_args_string()
            out_s = modport.get_out_str()
            in_s = modport.get_in_str()
            if in_s :
                in_s = "\n\t"+in_s
                if arg_s:
                    arg_s = '\n\t'+arg_s+",\n\t"
            if out_s:
                in_s= in_s+",\n\t"
            cont +=arg_s+ in_s+ out_s    
            cont += ");\n"
        cont += modport_str
        self.content += cont

    
class clock_code(uvm_code):
    
    def __init__(self,time = 5):
        super().__init__(None)  
        self.time = time
        self.tab_count =1
    def main_code(self):
        cont = ''
        cont+='initial begin\n'
        cont+='\tclk = 0;\n'
        cont+=f'\tforever #{self.time} clk = ~clk;\n'
        cont+='end\n'  
        self.content = cont       
    
class if_build_code(call_code):
    #输入为uvm_interface类
    def __init__(self, obj: uvm_interface,call:uvm_call,vif= None):
        super().__init__(obj,call)
        self.inter_if_name = "vif"
        if vif is not None:
            self.inter_if_name = obj.name
    
    def main_code(self):
        cont = ''
        vir = "virtual " if self.obj.virtual else ""
        cont+=f'if(!uvm_config_db #({vir}{self.obj.name})::get(null, "*","{self.inter_if_name}", {self.inter_if_name})) begin'
        cont+=f'\n\t`uvm_fatal(\"NO_VIF\", "Failed to get {self.obj.name}")\nend\n'

        self.content+=cont

class constraint_code(uvm_code):
    #输入为一个construct
    
    def main_code(self):
        k = "{\n}"
        l=[]
        for cons in self.obj.constraints.items():
            s = f"constraint {cons.name}{k}"
            l.append(s)
        ss = '\n'.join(l)
        
        self.content+=ss

class includes_code(uvm_code):
    
    def __init__(self, obj):
        super().__init__(obj)
        self.tab_count=0
    #输入是一个construct类
    def main_code(self):
        
        self.add_includes()
    
    def add_includes(self):
        cont = ''
        inc_s = "\n".join(self.obj.includes)
        cont+=inc_s
        self.content+= cont+"\n"  

class imports_code(uvm_code):
    
    def main_code(self):
        self.tab_count =1
        self.add_imports()
    
    def add_imports(self):
        cont = ''
        imp_s = "\n".join(self.obj.imports)
        cont+=imp_s
        if len(cont)>0:
            self.content+= cont+";\n"

class rst_code(uvm_code):
    
    def __init__(self):
        super().__init__(None)
        self.tab_count=1
    def main_code(self):
        cont = ''
        cont+="initial begin\n"
        cont+="\trst_n = 0;\n\t#25 rst_n = 1;\nend"
        self.content+=cont

class dut_connect_code(uvm_code):
    
    def __init__(self, dut,if_name=None):
        super().__init__(dut)
        self.if_name = if_name if if_name is not None else "vif"
        self.dut = dut
        self.tab_count= 1
    def main_code(self):
        cont=""
        cont+=self.dut.name+" u_dut(\n"
        w_l = []
        for w in self.obj.wires:
            w_s = f"\t.{w.name:<16}({self.if_name}.{w.name})"
            w_l.append(w_s)
        cont+=",\n".join(w_l)+"\n"+");\n"
        self.content+=cont
class top_if_new_code(uvm_code):
    #传入的是一个uvm_interface类
    def __init__(self,vif):
        super().__init__(vif)
        self.vif = vif
        self.tab_count =1
    
    def main_code(self):
        cont=""
        if_name = self.vif.name
        arg_l = []
        for key,value in self.vif.args_types:
            s = f".{key}({key})"
        arg_s = ",".join(arg_l)
        cont+=if_name+" "+f"vif({arg_s});\n\n"
        self.content+=cont
        
    