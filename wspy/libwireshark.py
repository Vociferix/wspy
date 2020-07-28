import ctypes
import ctypes.util
from wspy.errors import *

lib_name = ctypes.util.find_library('wireshark')
if lib_name is None:
    raise LibNotFound('wireshark')

libwireshark = ctypes.CDLL(lib_name)
