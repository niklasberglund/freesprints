import os

def isRunningOnRPi():
    if os.uname()[4][:3] == 'arm':
        return True
    else:
        return False
