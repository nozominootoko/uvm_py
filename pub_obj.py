all_objs = []
gnrl_genors = {}
def add_obj(obj):
    all_objs.append(obj)

def add_generator(name,generator):
    gnrl_genors[name] = generator

def clear_objs():
    all_objs.clear()
    
def get_objs():
    return all_objs

def pop_obj(obj):
    if obj in all_objs:
        all_objs.remove(obj)