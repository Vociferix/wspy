class Error(Exception):
    pass


class LibNotFound(Error):
    def __init__(self, libname):
        self.libname = libname
        self.message = 'Unable to find library: ' + libname


class LibError(Error):
    def __init__(self, libname, func, msg):
        self.libname = libname
        self.func = func
        self.message = func + ' (' + libname + '): ' + msg
