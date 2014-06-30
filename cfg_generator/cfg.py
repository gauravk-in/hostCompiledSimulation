import sys

class BBEdge:
    def __init__(self, fromBlockIndex, toBlockIndex):
        self.fromBlockIndex = fromBlockIndex;
        self.toBlockIndex = toBlockIndex;

class BasicBlock:
    def __init__(self, startLine, endLine):
        self.startLine = startLine;
        self.endLine = endLine;

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
        
 