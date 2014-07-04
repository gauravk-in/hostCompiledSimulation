import sys
from collections import deque
import logging

class ParseError(Exception):
    def __init__(self, str):
        self.value = str
    def __str__(self):
        return repr(self.value)

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
        self.flow = 0.0


class ControlFlowGraph:
    def __init__(self, listBlocks, listEdges):
        self.listBlocks = listBlocks
        self.listEdges = listEdges
        self.listBackEdges = []
        
    def successorBlocks(self, blockIndex):
        listSuccBlockIndices = []
        for edge in self.listEdges:
            if edge.fromBlockIndex == blockIndex:
                listSuccBlockIndices.append(edge.toBlockIndex)
        #logging.debug("Returns from successorBlocks(blockIndex)")
        return listSuccBlockIndices
    
    def successorBlocksWOBackEdges(self, blockIndex):
        listSuccBlockIndices = []
        edgeIndex = 0
        for edge in self.listEdges:
            if edge.fromBlockIndex == blockIndex and edgeIndex not in self.listBackEdges:
                listSuccBlockIndices.append(edge.toBlockIndex)
            edgeIndex = edgeIndex + 1
        return listSuccBlockIndices
    
    def successorBlocks(self, blockIndex):
        listSuccBlockIndices = []
        for edge in self.listEdges:
            if edge.fromBlockIndex == blockIndex:
                listSuccBlockIndices.append(edge.toBlockIndex)
        return listSuccBlockIndices
    
    def predecessorBlocksWOBackEdges(self, blockIndex):
        listPredBlockIndices = []
        edgeIndex = 0
        for edge in self.listEdges:
            if edge.toBlockIndex == blockIndex and edgeIndex not in self.listBackEdges:
                listPredBlockIndices.append(edge.toBlockIndex)
            edgeIndex = edgeIndex + 1
        logging.debug("returns from predecessorBlocksWOBackEdges(blockIndex)")
        return listPredBlockIndices
    
    def findEdgeIndex(self, fromBlockIndex, toBlockIndex):
        '''
        Returns index of edge in listEdges with given starting and ending blocks
        Return -1 if edge not found
        '''
        index = -1
        for edge in self.listEdges:
            index = index + 1
            if edge.fromBlockIndex == fromBlockIndex and edge.toBlockIndex == toBlockIndex:
                break
            
        return index

    # TODO Use a better name for this
    def dft(self, blockIndex):
        self.dft_stack.append(blockIndex)
        for succBlock in self.successorBlocksWOBackEdges(blockIndex):
            if succBlock not in self.dft_stack:
                self.dft(succBlock)
            else:
                self.listBackEdges.append(self.findEdgeIndex(blockIndex, succBlock))
        self.dft_stack.pop()
        
                
    def findBackEdges(self):
        '''
        Populate the list of Back Edges in the graph by traversing in 
        Depth First Fashion
        '''
        self.dft_stack = []
        self.dft(0)
        self.listBackEdges = list(set(self.listBackEdges))
        for edgeIndex in self.listBackEdges:
            print self.listEdges[edgeIndex].fromBlockIndex, self.listEdges[edgeIndex].toBlockIndex 
        return self.listBackEdges
    
    def computeFlow(self):
        '''
        Compute the flow value of each block in CFG of each function
        '''
        currBlockPredNotVisited = 0
        queuePending = deque([])
        self.findBackEdges()
        self.listBlocks[0].flow = 1.0
        for blockIndex in self.successorBlocksWOBackEdges(0):
            queuePending.append(blockIndex)
            
        while queuePending:
            currBlockIndex = queuePending.popleft()
            currBlockFlow = 0.0
            for predBlockIndex in self.predecessorBlocksWOBackEdges(currBlockIndex):
                if self.listBlocks[predBlockIndex].flow == 0:
                    # predecessor block still not visited
                    # add the current block back into queue, set flag and break from loop.
                    queuePending.append(currBlockIndex)
                    currBlockPredNotVisited = 1
                    break
                else:
                    currBlockFlow = currBlockFlow + (self.listBlocks[predBlockIndex].flow / len(self.successorBlocksWOBackEdges(predBlockIndex)))
                    
                if currBlockPredNotVisited == 1:
                    currBlockPredNotVisited = 0
                    continue
                else:
                    if currBlockFlow > 1.0:
                        raise ParseError("Flow in graph greater than 1!!")
                        exit(1)
                    else:
                        self.listBlocks[currBlockIndex].flow = currBlockFlow
        
class FunctionDesc:
    def __init__(self, functionName, fileName, startLine, endLine, cfg):
        self.functionName = functionName
        self.fileName = fileName
        self.startLine = startLine
        self.endLine = endLine
        self.cfg = cfg
        