import ctypes
import ctypes.util
from wspy.errors import *

lib_name = ctypes.util.find_library('wiretap')
if lib_name is None:
    raise LibNotFound('wiretap')

libwiretap = ctypes.CDLL(lib_name)
