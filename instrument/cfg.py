import sys
from collections import deque
import logging
from irc_regex import re_VarSpec

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
        self.mapsTo = []
        self.nestingLevel = -1
        self.hasConditionalExec = 0
        
    def mapISCTo(self, blockInd):
        # ISC Blocks will map to only one block in Obj
        self.mapsTo = [blockInd]


class ControlFlowGraph:
    def __init__(self, listBlocks, listEdges):
        self.listBlocks = listBlocks
        self.listEdges = listEdges
        self.listBackEdges = []
        
    def find(self, blockName=None, lineNum = None):
        if blockName:
            for block in self.listBlocks:
                if block.name == blockName:
                    return block
            return None
        
        if lineNum:
            for block in self.listBlocks:
                if block.startLine <= lineNum and block.endLine >= lineNum:
                    return block
            return None
        
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
    
    def predecessorBlocks(self, blockIndex):
        listSuccBlockIndices = []
        for edge in self.listEdges:
            if edge.toBlockIndex == blockIndex:
                listSuccBlockIndices.append(edge.fromBlockIndex)
        return listSuccBlockIndices
    
    def predecessorBlocksWOBackEdges(self, blockIndex):
        listPredBlockIndices = []
        edgeIndex = 0
        for edge in self.listEdges:
            if edge.toBlockIndex == blockIndex and edgeIndex not in self.listBackEdges:
                listPredBlockIndices.append(edge.fromBlockIndex)
            edgeIndex = edgeIndex + 1
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
            if self.listBlocks[succBlock].nestingLevel > self.listBlocks[blockIndex].nestingLevel or self.listBlocks[succBlock].nestingLevel == -1:
                self.listBlocks[succBlock].nestingLevel = self.listBlocks[blockIndex].nestingLevel + 1
            if succBlock not in self.dft_stack:
                self.dft(succBlock)
            else:
                # Awesome fix of an error identified during test
                # if a closed loop occurs consisting of multiple blocks, we
                #  need to remove all edges of the loop, because removing just
                #  the last edge will lead to flow being mis-calculated.
                # Remove edge from blockIndex to succBlock which has already
                #  visited.
                # Add the blockIndex to a queue.
                # Loop until queue is empty.
                #    Pop from queue in currBlock.
                #    if currBlock does not have any other successor,
                #        for each predecessor of currBlock, predBlock
                #            remove edge between predBlock and currBlock
                #            Add predBlock to queue
                self.listBackEdges.append(self.findEdgeIndex(blockIndex, succBlock))
                queueBlocksBackEdgesCheck = deque([blockIndex])
                while len(queueBlocksBackEdgesCheck) != 0:
                    currBlock = queueBlocksBackEdgesCheck.popleft()
                    if len(self.successorBlocksWOBackEdges(currBlock)) == 0:
                        for predBlock in self.predecessorBlocksWOBackEdges(currBlock):
                            self.listBackEdges.append(self.findEdgeIndex(predBlock, currBlock))
                            queueBlocksBackEdgesCheck.append(predBlock)
        self.dft_stack.pop()
        
                
    def findBackEdges(self):
        '''
        Populate the list of Back Edges in the graph by traversing in 
        Depth First Fashion
        '''
        self.dft_stack = []
        self.listBlocks[0].nestingLevel = 0
        self.dft(0)
        self.listBackEdges = list(set(self.listBackEdges))
        return self.listBackEdges
    
    def computeFlow(self):
        '''
        Compute the flow value of each block in CFG of each function
        '''
        currBlockPredNotVisited = 0
        queuePending = deque([])
        
        # Make a list of the back edges to be ignored while computing flow
        self.findBackEdges()
        # Set flow of starting block, and insert the successors in a queue
        self.listBlocks[0].flow = 1.0
        for blockIndex in self.successorBlocksWOBackEdges(0):
            queuePending.append(blockIndex)
            
        while queuePending:
            # treat each block in the queue
            currBlockIndex = queuePending.popleft()
            
            # Add the successors of the block to the queue
            for succBlockIndex in self.successorBlocksWOBackEdges(currBlockIndex):
                queuePending.append(succBlockIndex)
            
            # init flow to 0
            currBlockFlow = 0.0
            for predBlockIndex in self.predecessorBlocksWOBackEdges(currBlockIndex):
                # compute flow from predecessors
                if self.listBlocks[predBlockIndex].flow == 0:
                    # predecessor block still not visited
                    #     add the current block back into queue, 
                    #     set flag and break from loop.
                    queuePending.append(currBlockIndex)
                    currBlockPredNotVisited = 1
                    break
                else:
                    currBlockFlow = currBlockFlow + (self.listBlocks[predBlockIndex].flow / len(self.successorBlocksWOBackEdges(predBlockIndex)))

            # if flag set, reset it and continue                    
            if currBlockPredNotVisited == 1:
                currBlockPredNotVisited = 0
                continue
            else:
                if currBlockFlow > 1.0:
                    raise ParseError("Flow in graph greater than 1!!")
                    exit(1)
                else:
                    self.listBlocks[currBlockIndex].flow = currBlockFlow

class FunctionParam:
    def __init__(self, type, name, len, isPointer):
        self.type = type
        self.name = name
        self.len = len
        self.isPointer = isPointer
        
class FunctionDesc:
    def __init__(self, functionName, fileName, startLine, endLine, cfg, stackSize = -1, paramStr = None):
        self.functionName = functionName
        self.fileName = fileName
        self.startLine = startLine
        self.endLine = endLine
        self.cfg = cfg
        self.stackSize = stackSize
        self.paramStr = paramStr
        self.listParams = []
        if paramStr is not None and paramStr is not "":
            listParams = paramStr.split(",")
            for param in listParams:
                m = re_VarSpec.match(param)
                paramType = m.group("varType")
                paramName = m.group("varName")
                paramLen = m.group("varLen")
                if paramType.endswith("*") or paramLen is not "":
                    paramIsPointer = True
                else:
                    paramIsPointer = False
                self.listParams.append(FunctionParam(paramType, paramName, paramLen, paramIsPointer))        
        
            
    def setStackSize(self, stackSize):
        self.stackSize = stackSize
        