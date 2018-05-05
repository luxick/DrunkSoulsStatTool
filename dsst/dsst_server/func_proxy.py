from dsst_server.func_write import WriteFunctions
from dsst_server.func_read import ReadFunctions
from dsst_server.func_delete import DeleteFunctions


class FunctionProxy(WriteFunctions, ReadFunctions, DeleteFunctions):
    pass
