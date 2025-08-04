
from inspect import currentframe, getframeinfo

def dprint():
    def printfun(*args, **kwargs):
        frameinfo = getframeinfo(currentframe())
        print(f"{frameinfo.filename}: {frameinfo.lineno}", *args, **kwargs)
    return printfun
