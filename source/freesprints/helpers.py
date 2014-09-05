import os
import os.path

def isRunningOnRPi():
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