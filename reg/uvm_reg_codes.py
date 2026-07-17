from uvm_codes import call_code
from uvm_sv import uvm_code


class reg_new_code(call_code):
    #输入为一个uvm_reg对象和一个new函数
    def __init__(self,reg_obj,call ):
        super().__init__(reg_obj,call)  
        
    def main_code(self):
        cont=''     
        par = self.call.get_parent()
        c_str = "UVM_NO_COVERAGE"
        if par.has_coverage:
            c_str = "UVM_COVERAGE"
        cont += f'super.new(name,{par.n_bits},{c_str});'
        self.content = cont     

class reg_build_code(call_code):
    #输入为一个uvm_reg对象和一个new函数
    def __init__(self,reg_obj,call ):
        super().__init__(reg_obj,call)  
        
    def main_code(self):
        cont =''
        from reg.uvm_reg_field import uvm_reg_field
        par = self.call.get_parent()
        uvm_reg_fields= [child for child in par.get_children() if isinstance(child,uvm_reg_field)]
        create_str =[]
        for reg in uvm_reg_fields:
            name_str ="\""+ reg.name + "\""
            pcont = f"{reg.name:<8} = {reg.get_type_name()}::type_id::create({name_str:<10});"
            create_str.append(pcont)
        create_cont = "\n".join(create_str) + "\n"
        cont+=create_cont     + "\n"
        config_str = []
        for reg in uvm_reg_fields:
            access_str = "\""+ reg.m_access + "\""
            pcont = f"{reg.name:>8}.configure(this, {reg.m_size}, {reg.m_lsb}, {access_str:>5}, {reg.m_volatile}, {reg.p_reset}, {reg.p_has_reset}, {reg.p_is_rand}, {reg.p_in_acc});"
            config_str.append(pcont)
        config_cont = "\n".join(config_str) + "\n"
        cont+=config_cont    + "\n" 
        self.content += cont     

class reg_block_build_code(call_code):
    #输入为一个uvm_reg_block对象和一个new函数
    def __init__(self,reg_obj,call ):
        super().__init__(reg_obj,call)  
        
    def main_code(self):

        from reg.uvm_reg import uvm_reg
        cont=''+"\n"
        par = self.obj
        uvm_regs= [child for child in par.get_children() if isinstance(child,uvm_reg)]
        create_str =[]
        for reg in uvm_regs:
            pcont = f"{reg.name:<12} = {reg.get_type_name()}::type_id::create(\"{reg.name}\",,get_full_name());"
            create_str.append(pcont)
        create_cont = "\n".join(create_str)
        cont+=create_cont + "\n\n"
        
        config_str = []
        for reg in uvm_regs:
            pcont = f"{reg.name}.configure(this);"
            config_str.append(pcont)
        config_cont = "\n".join(config_str) + "\n"
        cont+=config_cont + "\n"
        
        build_str = []
        for reg in uvm_regs:
            pcont = f"{reg.name}.build();"
            build_str.append(pcont)   
        build_cont = "\n".join(build_str) + "\n"
        cont+=build_cont + "\n"
        
        map_create = f"default_map = create_map(\"default_map\", 'h0, 4, UVM_LITTLE_ENDIAN, 1);\n"
        map_str =[]
        for reg in uvm_regs:
            addr_s = ''
            if reg.reg_addr is not None:
                addr_s = reg.reg_addr
            pcont = f"default_map.add_reg({reg.name:<12},{addr_s},\"RW\");"
            map_str.append(pcont)
        map_cont = map_create+"\n".join(map_str) + "\n"
        cont+=map_cont + "\n"
        self.content+=cont      

class reg_block_new_code(call_code):
    #输入为一个uvm_reg对象和一个new函数
    def __init__(self,reg_obj,call ):
        super().__init__(reg_obj,call)  
        
    def main_code(self):
        from reg.uvm_reg_field import uvm_reg_field
        cont=''    
        par = self.call.get_parent()
        c_str = "UVM_NO_COVERAGE"
        if par.has_coverage:
            c_str = "UVM_COVERAGE"
        cont += f'super.new(name,{c_str});'
        self.content = cont     
     