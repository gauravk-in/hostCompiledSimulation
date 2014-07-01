import sys

class BBEdge:
    def __init__(self, fromBlockIndex, toBlockIndex):
        self.fromBlockIndex = fromBlockIndex;
        self.toBlockIndex = toBlockIndex;

class BasicBlock:
    def __init__(self, startLine, endLine, isReturning=0, listFuncCalls = None, name = None):
        if name is None:
            self.name = ""
        else:
            self.name = name
        self.startLine = startLine
        self.endLine = endLine
        self.isReturning = isReturning
        if listFuncCalls is None:
            self.listFunctionCalls = []
        else:
            self.listFunctionCalls = listFuncCalls

class ControlFlowGraph:
    def __init__(self, listBlocks, listEdges):
        self.listBlocks = listBlocks
        self.listEdges = listEdges
        
class FunctionDesc:
    def __init__(self, functionName, fileName, startLine, endLine, cfg):
        self.functionName = functionName
        self.fileName = fileName
        self.startLine = startLine
        self.endLine = endLine
        self.cfg = cfg
        