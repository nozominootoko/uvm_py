
from base.uvm_object import uvm_object
from reg.uvm_reg_codes import reg_build_code, reg_new_code
from reg.uvm_reg_field import uvm_reg_field
from uvm_call import uvm_function



class uvm_reg(uvm_object):
    def __init__(self, name: str = "", n_bits: int = 0, has_coverage: bool = False):
        super().__init__(name)
        from reg.uvm_reg_block import uvm_reg_block
        self.m_locked: bool 
        self.m_parent: uvm_reg_block
        self.new_func = uvm_function("new",self).add_args("string","name","\""+self.name+"\"").set_return_type("")
        self.new_func.add_code(reg_new_code(self,self.new_func))
        self.build_func = uvm_function("build",self).set_virtual()
        self.build_func.add_code(reg_build_code(self,self.build_func))
        
        self.m_fields = []
        self.n_bits = n_bits
        self.has_coverage = has_coverage
        self.gen_file = True
        self.reg_addr = None
        
    def add_field(self,rf:uvm_reg_field):
        self.m_fields.append(rf)
    
    def get_genor_type(self):
        
        return "reg_genor"
    
    def __call__(self, name, parent,addr):

        #当时使用这个方法时，会创建出一个新的对象，并将其父对象设置为parent
        new_obj = self.__class__(name, self.n_bits,self.has_coverage)
        new_obj.reg_addr = addr
        self.parent = parent
        self.parent.add_child(new_obj)
        new_obj.set_gen_file(False)
        new_obj.class_name = self.name
        #会将老对象中的属性和方法复制到新对象中
        for child in self.kids.values():
            new_obj.add_child(child)    
        return new_obj