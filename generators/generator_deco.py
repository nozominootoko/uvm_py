# 创建一个生成器的装饰器，使被装饰的类可以自动创建本身的生成器对象



def generator_regi(name=None):
    """装饰器工厂：返回一个装饰器对象。

    用法：
      @generator_gen(name="component_generator")
      class MyGen: ...
    """
    def _decorator(cls):
        from base_genor import base_genor
        if not issubclass(cls,base_genor):
            raise TypeError(f"Class {cls.__name__} is not a generator.")
        from pub_obj import add_generator
        # 创建一个生成器对象，并将其作为类属性添加到被装饰的类中
        genor = cls()
        # 避免在内部函数中给外层参数赋值导致 UnboundLocalError
        gen_name = name if name is not None else cls.__name__.lower()
        add_generator(gen_name, genor)
        
        return cls

    return _decorator