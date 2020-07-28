from ctypes import *


def c_va_list(*argv):
    args = []
    types = []
    for arg in argv:
        args.append(arg)
        types.append(type(arg))
    return (args, types)
