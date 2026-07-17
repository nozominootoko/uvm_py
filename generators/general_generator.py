

from base_genor import construct_genor
from pub_obj import get_objs, pop_obj
from collections.abc import Iterable



class general_generator(construct_genor):
    '''
    在生成uvm_object对象时，自动将生成的对象添加到上述的all_kids列表中，方便后续对生成的对象进行操作
    '''
    
    def __init__(self):
        super().__init__()
        #用词典管理生成器对象，方便后续根据对象类型调用对应的生成器对象
        from pub_obj import gnrl_genors
        self.genor_dict = gnrl_genors
        self.file_name = "grl.sv" #生成的文件名
    def set_one_time(self, one_time: bool):
        '''
        避免生成文件
        '''
        
        for genor in self.genor_dict.values():
            genor.one_time = one_time
        self.one_time = one_time
    def set_gen_file(self,gen_file:bool):
        '''
        设置是否生成文件
        '''
        self.gen_file = gen_file
        for genor in self.genor_dict.values():
            genor.gen_file = gen_file
    def clear_content(self):
        '''
        清空生成内容
        '''
        for genor in self.genor_dict.values():
            genor.content = ""
    def before_generate(self,object):
        if object is not None and not isinstance(object, list):
            self.file_name = f"{object.get_name()}.sv"

    def  generate(self, object = None):
        self.obj = object
        self.before_generate(object)
        self.run_generate(object)
        self.after_generate()    
        return self.content
    def run_generate(self, obj = None):
        if obj is None:
            # 使用 all_objs 列表中的对象进行生成（批量生成时统一设置 one_time=False）
            self.set_one_time(True)
            self.gen_file = False
            for o in get_objs():   
                # print(f"name:{o.name},gen_file{o.gen_file},genor_type:{o.get_genor_type()}")          
                genor = self.genor_dict.get(o.get_genor_type())
                genor.gen_file = o.gen_file
                
                self.content += genor.generate(o)
        elif isinstance(obj, Iterable) and not isinstance(obj, (str, bytes, bytearray)):
            # 如果传入的是一个对象列表/集合/元组等可迭代对象，则设置 one_time 为 False
            self.set_one_time(False)
            for o in obj:
                genor = self.genor_dict.get(o.get_genor_type())
                genor.gen_file = o.gen_file
                self.content += genor.generate(o)
                genor.content = ""
                pop_obj(o)
        else:
            self.content += self.genor_dict[obj.get_genor_type()].generate(obj)