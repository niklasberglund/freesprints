import os
import os.path

def is_running_on_rpi():
    if os.uname()[4][:3] == 'arm':
        return True
    else:
        return False


def rootPath():
    return os.getcwd()
    #return os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    # os.path.dirname(os.path.realpath(__file__))

def pluginsPath():
    return os.path.abspath(os.path.join(rootPath(), "plugins"))

def string_representation(object, variable_dict):
    str = "({0}):".format(object.__class__)
    i = 0
    for key in variable_dict:
        str = str + "\n\t{0} = {1}".format(key, variable_dict[key])
        i = i+1
    
    return str
