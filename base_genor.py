from generators.generator_deco import generator_regi
from uvm_codes import constraint_code, gen_call_code, constr_head_code, declare_code, imports_code, includes_code
from uvm_sv import uvm_sv
import uvm_config

class base_genor:
    def __init__(self):
        
        self.content = ""
        self.one_time = True #是否只生成一次，默认为True，如果需要多次生成则设置为False
        self.gen_code = True #是否生成代码，默认为True，如果不需要生成代码
        self.obj:uvm_sv = None #生成代码的对象，可以是uvm_sv的子类对象，如果不需要生成代码则为None
        self.no_gen = False #是否不生成代码，默认为False，如果需要不生成代码则设置为True
        self.gen_file = True #是否生成文件，默认为True，如果不需要生成文件则设置为False
        
        self.prepare()
    def add_codes_str(self):
        cont= '\n'
        for code in self.obj._uvm_codes:
            cont+=code.gen_code()
        return cont+"\n"
    def prepare(self):
        
        pass
    
    def before_generate(self):
        if self.one_time:
            self.content = "" #清空内容
        self.file_name = f"{self.obj.get_name()}.sv"
    
    def generate(self,obj):
        if self.no_gen:
            return ""
        self.obj = obj
        self.before_generate()
        self.run_generate()
        self.after_generate()
        return self.content
    def run_generate(self, object):
        pass
    
    def after_generate(self):
        pass
    
    def add_to_content(self, code:str):
        self.content += code

@generator_regi(name="void_genor")
class void_generator(base_genor):
    '''
    用于生成不需要生成文件的uvm组类
    '''
    def __init__(self):
        super().__init__()
        self.no_gen = True

class file_generator(base_genor):
    '''
    用于生成需要生成文件的uvm组类
    '''
    def __init__(self):
        super().__init__()
        self.gen_file = True
        self.file_path = uvm_config.dir_path

    def run_generate(self):
        
        self._generate_content()
        
    def _generate_content(self):
        # if self.one_time:
        #     self.add_to_content(self.generate_file_head())
        self.inter_content() 
        
        # if self.one_time:
        #     self.add_to_content(self.generate_file_tail())   
    def inter_content(self):
        pass    
    def generate_file_head(self)-> str:
        ifndef_cont = "`ifndef"
        define_cont_start = "`define"      

        row_1 = f"{ifndef_cont} {self.file_name.replace('.', '_').upper()}\n"
        row_2 = f"{define_cont_start} {self.file_name.replace('.', '_').upper()}\n\n"
        file_head = row_1 + row_2
        return file_head  
    
    def generate_file_tail(self)-> str:
        cont=''
        cont += f"`endif // {self.file_name.replace('.', '_').upper()}\n"
        return cont
    
    def after_generate(self):
        import pathlib as pl
        if self.file_path is not None and self.gen_file and self.one_time:
            dir_path = pl.Path(self.file_path) 
            dir_path.mkdir(parents=True, exist_ok=True)#生成文件所在目录
            file_path = pl.Path(self.file_path) / self.file_name #生成文件路径
            self.file = open(file_path, 'w',encoding='utf-8') #打开文件
            self.file.write(self.content) #写入内容
            self.file.close() #关闭文件
    def to_file(self,file_name = "default.sv"):
        import pathlib as pl

        if self.gen_file and not self.one_time:
            
            dir_path = pl.Path(self.file_path) 
            dir_path.mkdir(parents=True, exist_ok=True)#生成文件所在目录
            if file_name is not None:
                self.file_name = file_name
            file_path = pl.Path(self.file_path) / self.file_name #生成文件路径
            self.file = open(file_path, 'w',encoding='utf-8') #打开文件
            self.file.write(self.content) #写入内容
            self.file.close() #关闭文件    
@generator_regi(name="construct_genor")    
class construct_genor(file_generator):
    '''
    用于生成构造函数的生成器
    '''
    def __init__(self):
        super().__init__()
        self.out_constr_content = "" #构造函数外的内容
        
    def inter_content(self):
        self.add_to_content(self.generate_before_constr())
        self.add_to_content(self.add_incs())
        self.add_to_content(self.generate_constr_head())
        self.add_to_content(self.add_imps())
        self.add_to_content(self.generate_children_constr())
        self.add_to_content(self.generate_other_children_constr())
        
        self.add_to_content(self.uvm_utils())
        self.add_to_content(self.add_codes_str())
        self.add_to_content(self.generate_calls())
        self.add_to_content(self.end_of_constr()) 
        self.add_to_content(self.generate_out_constr()) 
    def add_imps(self):
        im_c = imports_code(self.obj)
        return im_c.gen_code()   
    def add_incs(self):
        i_code = includes_code(self.obj)
        i_code.tab_count =0
        return i_code.gen_code()             
    def generate_other_children_constr(self):
        return ""
    def generate_before_constr(self):
        cont ="\n".join(self.obj.before_class_content)
        return cont
    def generate_constr_head(self):
        code = constr_head_code(self.obj)
        return code.gen_code()
        
    
    def generate_children_constr(self):
        #生成对象的声明
        cont = ""
        for child in self.obj.get_children():
            constr_code = declare_code(child)
            cont += constr_code.gen_code()  
        for name, pro in self.obj.properties.items():

            constr_code = declare_code(pro)
            cont += constr_code.gen_code() 
        cc =  constraint_code(self.obj)
        cont+=cc.gen_code()     
        return cont
    def uvm_utils(self):
        return ""
    
    def generate_calls(self):
        cont = ''
        calls = self.obj.calls.items()
        for name,call in calls:
            coder = gen_call_code(call)
            cont += coder.gen_code()
            self.out_constr_content += coder.out_constr_content
            if not call.extern:
                cont+="\n"
        return cont
    
    def generate_out_constr(self) -> str:
        cont = ''
        cont = self.out_constr_content
        return cont                  
    def end_of_constr(self):
        return f"\nend{self.obj.contruct_type}: {self.obj.get_name()}\n\n"             
        
    def to_file(self,file_name = None):
        #添加文件头
        self.file_name = file_name if file_name else self.file_name
        self.content= self.generate_file_head() + self.content
        self.content+=self.generate_file_tail()
        super().to_file(file_name)