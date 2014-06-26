#-----------------------------------------------------------------
# construct_cfg_binary.py : Construct Control Flow Graph by parsing
#         the objdump of the binary
#-----------------------------------------------------------------
# from __future__ import print_function
import sys
import re

re_sectionStart = re.compile('Disassembly of section .(.*):')
re_Declaration = re.compile('\s*([0-9a-f]*)\s*<(.*)>:')
re_instruction = re.compile('\s*([0-9a-f]*):\s*([0-9a-f])*\s*(.*)')
re_unconditionalBranchInst = re.compile('\s*(b(?:l|x|lx|xj)?)\s*([0-9a-f]*)\s*<(.*)>')
re_conditionalBranchInst = re.compile('\s*(b(?:l|x|lx|xj)?(?:eq|ne|mi|pl|hi|ls|ge|lt|gt|le))\s*([0-9a-f]*)\s*<(.*)>')
re_returnInst = re.compile('\s*(bx)\s*(lr)')
re_startWithSemiColon = re.compile('\s*_+.*')

# Dictionary to record line number for relative address in the code
lineForRelAdd = {}
# Dictionary to record the branch instructions at an address
branchInstAtAdd = {}

# Address of the first instruction of the code
mainStartAddress = 0
mainEndAdresses = []

# Address of the current function block
currentFunctionName = ""
currentFunctionBodyStartAdd = 0
currentFunctionBodyEndAdd = 0
listCurrentFunctionReturnInstAdd = []

# List to maintain start addresses of the basic blocks
listBlockStartAdd = []
listBlockEndAdd= []

listFunctionsIgnore = ['__cs3_interrupt_vector',
                        '__cs3_reset',
                        '__cs3_start_asm_sim',
                        '__cs3_heap_start_ptr',
                        '__cs3_start_c',
                        '__do_global_dtors_aux',
                        'frame_dummy',
                        'atexit',
                        'exit',
                        '__register_exitproc',
                        '__call_exitprocs',
                        'register_fini',
                        '__libc_fini_array',
                        '__cs3_premain',
                        '_exit',
                        '__cs3_isr_interrupt',
                        '__libc_init_array']

class ParseError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class FunctionBody:
    def __init__(self, functionName, startAdd, endAdd, listReturnInstAdd):
        self.name = functionName
        self.startAdd = startAdd
        self.endAdd = endAdd
        self.startLine = lineForRelAdd[startAdd]
        self.endLine = lineForRelAdd[endAdd]
        self.listReturnInstAdd = listReturnInstAdd

# List of function bodies
listFunctionBodies = []
listBasicBlocks = []

class BasicBlock:
    startLine = 0
    endLine = 0
    startAdd = 0
    endAdd = 0
    
    def __init__(self, startAdd, endAdd):
        self.startLine = lineForRelAdd[startAdd]
        self.endLine = lineForRelAdd[endAdd]
        self.startAdd = startAdd
        self.endAdd = endAdd
        
class BBEdge:
    def __init__(self, startBlockIndex, endBlockIndex):
        self.startBlockIndex = startBlockIndex
        self.endBlockIndex = endBlockIndex 
        
class ControlFlowGraph:
    def __init__(self, listBlocks, listEdges):
        self.listBlocks = listBlocks
        self.listEdges = listEdges
        
    def addBlock(self, block):
        self.listBlocks.append(block);
        
    def addEdge(self, branchInstAdd, branchTargetAdd):
        edgeStartBlockIndex = -1
        edgeEndBlockIndex = -1
        
        for i in range(len(self.listBlocks)):
            if(self.listBlocks[i].endAdd == branchInstAdd):
                edgeStartBlockIndex = i
            if(self.listBlocks[i].startAdd == branchTargetAdd):
                edgeEndBlockIndex = i
        
        if edgeStartBlockIndex == -1 or edgeEndBlockIndex == -1:
            return
        
        edge = BBEdge(edgeStartBlockIndex, edgeEndBlockIndex)
        if edge not in self.listEdges:
            self.listEdges.append(edge)
            
    def populateEdges(self):
        for block in self.listBlocks:
            blockEndAdd = block.endAdd
            if blockEndAdd in branchInstAtAdd:
                m = re_unconditionalBranchInst.match(branchInstAtAdd[blockEndAdd])
                if m is not None:
                    # unconditional branch, add edge to target but not to next instruction
                    self.addEdge(blockEndAdd, m.group(2))
                else:
                    m = re_conditionalBranchInst.match(branchInstAtAdd[blockEndAdd])
                    if m is not None:
                        # conditional branch, add edge to target and next instruction
                        self.addEdge(blockEndAdd, m.group(2))
                        self.addEdge(blockEndAdd, "%x" % (int(blockEndAdd, 16) + 4))
                    else:
                        m = re_returnInst.match(branchInstAtAdd[blockEndAdd])
                        if m is not None:
                            continue
            else:
                self.addEdge(blockEndAdd, "%x" % (int(blockEndAdd, 16) + 4))

        # For return instructions
        # Fucking Ugly Code
        for address in branchInstAtAdd:
            m = re_unconditionalBranchInst.match(branchInstAtAdd[address])
            if m is not None:
                targetAddress = m.group(2)
                for funcBody in listFunctionBodies:
                    if targetAddress == funcBody.startAdd:
                        for retInstAdd in funcBody.listReturnInstAdd:
                            self.addEdge(retInstAdd, "%x" % (int(address, 16) + 4))
                        
    
    def print_debug(self):
        for i in range(len(self.listBlocks)):
            print "Block "+str(i)+": "+self.listBlocks[i].startAdd+" - "+self.listBlocks[i].endAdd
            for edge in self.listEdges:
                if edge.startBlockIndex == i:
                    print "\t Edge to block"+str(edge.endBlockIndex)
            
      
def compareHexStrings(x, y):
    if int(x, 16) < int(y, 16):
        return -1
    elif int(x, 16) == int(y, 16):
        return 0
    else:
        return 1      


def construct_cfg_binary(filename):
    global listBlockStartAdd
    global listBlockEndAdd
    global currentFunctionName
    global currentFunctionBodyStartAdd
    global currentFunctionBodyEndAdd
    global listCurrentFunctionReturnInstAdd
    
    file = open(filename, 'r')
    inFunctionBody = 0
    in_text_section = 0
    line_num = 0
    
    for line in file:
        '''
        Loop that reads each line, and parses the code. 
        The basic algorithm,
        1. Read each line, look for the .text section.
        2. Find start of function bodies, the following lines
            are instructions. Keep track of start of function body
            and name of the function. Skip functions from the libc.
        3. Each instruction is read in matched_codeLine function.
            Here we keep two arrays with address of start and end
            of Basic Blocks:
            a. First instruction in a function is a start of BB.
            b. Each Branch instruction is end of a BB.
            c. Target of Branch instruction is start of BB.
            d. Instruction before Branch target is end of BB.
            e. Instruction after Branch instruction is start of BB.
            f. Return instructions are end of basic blocks.
            g. Additionally, make a dictionary for address to 
                Branch instruction for each Branch instruction.
        4. Once we have the BB borders, we will start creating the
            graph.
            a. Find main function in list of function bodies, the root
                of the graph is first basic block in the main function.
            b. For function calls, keep a stack of functions called.
            c. Iterate through the dictionary of branch instructions,
                1. If branch target points to address in current function,
                    make an edge to the block with same start address.
                2. If branch target points to address in another function,
                    create an edge to the corresponding basic block and
                    an edge from all return instruction in the function
                    to the instruction next to the branch instruction.
                    
        '''
        line_num = line_num + 1
        # Algo 1.
        # Look for start of sections
        m = re_sectionStart.match(line)
        if m is not None and m.group(1) == "text":
            in_text_section = 1
            continue
        elif m is not None and m.group(1) != "text":
            in_text_section = 0
            continue
        
        
        if in_text_section == 1:
            # Algo 2.
            # if not in function body
            if inFunctionBody == 0:
                # Look for start of function body
                m = re_Declaration.match(line)
                # TODO: Looking at functions not starting with semi colon only
                #    doing it so as to avoid bx r3 type of instructions
                if m is not None and m.group(2) not in listFunctionsIgnore:
                    currentFunctionName = m.group(2)
                    # initialize following after reading next instruction
                    currentFunctionBodyStartAdd = -1
                    inFunctionBody = 1;
                    continue
            # Algo 3.
            # else, if in function body        
            else:
                m = re_instruction.match(line)
                if m is not None:
                    lineForRelAdd[m.group(1)] = line_num
                    matched_codeLine(m.group(1), m.group(3))
                    currentFunctionBodyEndAdd = m.group(1)
                else:
                    listFunctionBodies.append(FunctionBody(currentFunctionName,
                                                          currentFunctionBodyStartAdd,
                                                          currentFunctionBodyEndAdd,
                                                          listCurrentFunctionReturnInstAdd))
                    listCurrentFunctionReturnInstAdd = []
                    inFunctionBody = 0
                    
                    
    # Code has been parsed
    # A list of start and end addresses of basic blocks prepared
    # remove duplicates
    listBlockStartAdd = list(set(listBlockStartAdd))
    listBlockStartAdd.sort(cmp = compareHexStrings)
    listBlockEndAdd = list(set(listBlockEndAdd))
    listBlockEndAdd.sort(cmp = compareHexStrings)
    
    if(len(listBlockStartAdd) != len(listBlockEndAdd)):
        raise ParseError('Length of Block Start and End Addresses not equal')

    cfg = ControlFlowGraph([], [])
    for i in range(len(listBlockStartAdd)):
        cfg.addBlock(BasicBlock(listBlockStartAdd[i], listBlockEndAdd[i]))
        
    cfg.populateEdges()
    return cfg

                    
def matched_codeLine(address, inst):
    '''
    Function to parse each instruction in the function body
    '''
    global currentFunctionBodyStartAdd
    global listCurrentFunctionReturnInstAdd
    
    if currentFunctionBodyStartAdd == -1:
        currentFunctionBodyStartAdd = address
        #Algo 3.a
        listBlockStartAdd.append(address)
        
    m = re_conditionalBranchInst.match(inst)
    if m is not None:
        branchInstAtAdd[address] = inst;
        # Algo 3.b. End of a Basic Block at branch
        listBlockEndAdd.append(address)
        # Algo 3.c. Start of a basic block from target address of branch inst.
        listBlockStartAdd.append(m.group(2))
        # Algo 3.d. End of a basic block at inst before target address of branch
        if m.group(3).startswith(currentFunctionName):
            listBlockEndAdd.append("%x" % (int(m.group(2), 16) - 4))
        # Algo 3.e Start of a basic block from next inst to the branch inst.
        addOfNextInst = "%x" % (int(address, 16) + 4)
        listBlockStartAdd.append(addOfNextInst)
        
    m = re_unconditionalBranchInst.match(inst)
    if m is not None:
        branchInstAtAdd[address] = inst;
        # Algo 3.b. End of a Basic Block at branch
        listBlockEndAdd.append(address)
        # Algo 3.c. Start of a basic block from target address of branch inst.
        listBlockStartAdd.append(m.group(2))
        # Algo 3.d. End of a basic block at inst before target address of branch
        if m.group(3).startswith(currentFunctionName):
            listBlockEndAdd.append("%x" % (int(m.group(2), 16) - 4))
        # Algo 3.e Start of a basic block from next inst to the branch inst.
        addOfNextInst = "%x" % (int(address, 16) + 4)
        listBlockStartAdd.append(addOfNextInst)

    m = re_returnInst.match(inst)    
    if m is not None:
        branchInstAtAdd[address] = inst;
        listCurrentFunctionReturnInstAdd.append(address)
        # Algo 3.f End of a Basic Block
        listBlockEndAdd.append(address)


    
if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename  = sys.argv[1]
    else:
        print('Usage: \n\t python %s <objdump_filename>' % (sys.argv[0]))
        exit(0)

    cfg = construct_cfg_binary(filename)
#     print lineForRelAdd
#     for inst in branchInstAtAdd.itervalues(): 
#         print inst 
#     print listBlockStartAdd
#     print listBlockEndAdd
#     print len(listBlockStartAdd)
#     print len(listBlockEndAdd)
#     for b in listFunctionBodies:
#         print b.name
#         for retInstAdd in b.listReturnInstAdd:
#             print "\t"+retInstAdd
    cfg.print_debug()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    