from dsst_server.func_write import WriteFunctions
from dsst_server.func_read import ReadFunctions


class FunctionProxy(WriteFunctions, ReadFunctions):
    pass
