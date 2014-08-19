import re
import sys
from subprocess import call

from cfg import *

gdbBin = "arm-none-eabi-gdb"

def find(f, seq):
    """Return first item in sequence where f(item) == True."""
    for item in seq:
        if f(item): 
            return item

class GlobalVariable:
    def __init__(self):
        self.name = ""
        self.address = 0
        self.type = ""
        self.length = -1
        self.size = -1
        self.file = ""
        self.lineNum = -1
        
    def __init__(self, name, type, length, file):
        self.name = name
        self.address = -1
        self.type = type
        self.length = length
        self.file = file
        self.lineNum = -1
        
    def setAddress(self, address):
        self.address = address
        
    def setSize(self, size):
        self.size = size
        
    def debug(self):
        print ("%s\t\t0x%x\t\t(type=%s; size=%d) - %s" % 
               (self.name, self.address, self.type, self.size, 
                self.file))


def debugListGlobalVariables(listGlobalVariables):
    print ""
    for globVar in listGlobalVariables:
        globVar.debug()
    print ""


def getGlobalVariablesInfoFromGDB(listBinaryFileNames):
    
    re_AllDefinedVariables = re.compile("All Defined Variables:")
    re_FullFileName = re.compile("/?(?:.*/)*(?P<fName>.*)")
    re_File = re.compile("File\s(.*):")
    re_Variable = re.compile("((?:[\w_]*\s)*)([\w_]*)(?:\[([0-9]*)\])*;")
    re_VarAdd = re.compile("Symbol \"(?P<varName>[\w_]*)\" is static storage at address (?P<varAdd>[0-9a-fA-Fx]*).")
    re_VarSize = re.compile("\s*sizeof\((?P<varName>[\w_]*)\) = (?P<varSize>\d*)")
    
    listGlobalVariables = []
    
    for fileName in listBinaryFileNames:
        m = re_FullFileName.match(fileName)
        if m is not None:
            fName = m.group("fName")
        else:
            logging.error("Filename could not be matched! - %s\n" % (fileName))
            return None
        
        # Fetch Global Variable Names from this file
        gdbXFileName = "/tmp/" + fName + ".globalVarNames.gdbx"
        gdbXFile = open(gdbXFileName, 'w')
        
        command = "info variables\n"
        gdbXFile.write(command)
        gdbXFile.write("quit\n")
        gdbXFile.close()
        
        gdbOFileName = "/tmp/" + fName + ".globalVarNames.gdbo"
        gdbOFile = open(gdbOFileName, 'w')
        call(args=[gdbBin, "--quiet", "--command="+gdbXFileName, fileName], 
             stdout=gdbOFile)
        gdbOFile.close()
        
        gdbOFile = open(gdbOFileName, 'r')
        currFileName = ""
        currListGlobalVariables = []
        for line in gdbOFile:
            m = re_File.match(line)
            if m is not None:
                currFileName = m.group(1)
                continue
            
            m = re_Variable.match(line)
            if m is not None:
                dataType = m.group(1)
                varName = m.group(2)
                if m.group(3) is not None:
                    varLen = int(m.group(3))
                else:
                    varLen = 1
                currListGlobalVariables.append(GlobalVariable(name=varName,
                                                          type=dataType,
                                                          length=varLen,
                                                          file=currFileName))
        gdbOFile.close()
        
        # Fetch addresses for Global Variables in this file
        gdbXFileName = "/tmp/" + fName + ".globalVarAdd.gdbx"
        gdbXFile = open(gdbXFileName, 'w')
            
        for var in currListGlobalVariables:
            gdbXFile.write("info address %s\n" % (var.name))
            gdbXFile.write("printf \"sizeof(%s) = %s\\n\", sizeof(%s)\n" % (var.name, "%d", var.name))
        
        gdbXFile.write("quit\n")
        gdbXFile.close()
        
        gdbOFileName = "/tmp/" + fName + ".globalVarAdd.gdbo"
        gdbOFile = open(gdbOFileName, 'w')
        call(args=[gdbBin, "--quiet", "--command="+gdbXFileName, fileName], 
             stdout=gdbOFile)
        gdbOFile.close()
        
        gdbOFile = open(gdbOFileName, 'r')
        for line in gdbOFile:
            m = re_VarAdd.match(line)
            if m is not None:
                varName = m.group("varName")
                varAdd = int(m.group("varAdd"), 16)
                var = find(lambda v: v.name == varName, currListGlobalVariables)
                var.setAddress(varAdd)
                continue
                
            m = re_VarSize.match(line)
            if m is not None:
                varName = m.group("varName")
                varSize = int(m.group("varSize"))
                var = find(lambda v: v.name == varName, currListGlobalVariables)
                var.setSize(varSize)
                continue
        
        gdbOFile.close()
        
        listGlobalVariables = listGlobalVariables + currListGlobalVariables
    
    debugListGlobalVariables(listGlobalVariables)
    return listGlobalVariables


class LocalVariable:
    def __init__(self, name, address, type, size, funcName):
        self.name = name
        self.type = type
        self.address = address
        self.funcName = funcName
        self.size = size
        
    def debug(self):
        logging.debug("LocalVar %s in func %s, address = %d, type = \"%s\", size = %d" % 
                      (self.name, self.funcName, self.address, self.type, self.size))

def debugPrintListLocalVariables(listLocalVariables):
    for var in listLocalVariables:
        var.debug()
    print ""

def getLocalVariablesForAllFunc(listBinaryFileNames, listFunctionsObj):
    binaryFileName = listBinaryFileNames[0]    
    
    VarValTypes = "(?P<valTypeOptOut>\<value optimized out\>)|\{.*\}|.*"
    re_LocalVar = re.compile("\s*(?P<varName>\w*)\s*=\s*(?:%s)" % (VarValTypes))
    re_InfoScope = re.compile("\s*Symbol (?P<varName>\w*) is (?P<varType>.*), length (?P<length>\d*).")
    re_SPLine = re.compile("\s*SP = (?P<valSP>[a-f0-9]*)")
    re_LocalVarLine = re.compile("\s*LocalVar: (?P<varName>\w*)")
    re_addressLine = re.compile("\s*address = 0x(?P<address>[a-f0-9]*)")
    re_typeLine = re.compile("\s*type = (?P<varType>.*)")
    re_sizeLine = re.compile("\s*size = (?P<varSize>[\d*])")
    
    listLocalVariables = []
    
    for func in listFunctionsObj:
        gdbXFileName = "/tmp/" + func.functionName + ".lVarName.gdbx"
        gdbOFileName = "/tmp/" + func.functionName + ".lVarName.gdbo"
        
        gdbXFile = open(gdbXFileName, 'w')
        gdbXFile.write("target sim\n")
        gdbXFile.write("load\n")
        gdbXFile.write("b %s\n" % func.functionName)
        gdbXFile.write("commands\n")
        gdbXFile.write("\tinfo locals\n")
        gdbXFile.write("end\n")
        gdbXFile.write("run\n")
        gdbXFile.write("quit\n")
        gdbXFile.close()

        gdbOFile = open(gdbOFileName, 'w')
        call(args=[gdbBin, "--quiet", "--command="+gdbXFileName, binaryFileName],
             stdout=gdbOFile)
        gdbOFile.close()
        
        listLocalVarNames = []
        gdbOFile = open(gdbOFileName, 'r')
        for line in gdbOFile:
            m = re_LocalVar.match(line)
            if m is not None:
                if m.group("valTypeOptOut") is None:
                    varName = m.group("varName")
                    listLocalVarNames.append(varName)
        gdbOFile.close()
        
        gdbXFile = open(gdbXFileName, 'w')
        gdbXFile.write("target sim\n")
        gdbXFile.write("load\n")
        gdbXFile.write("info scope %s\n" % func.functionName)
        gdbXFile.write("quit\n")
        gdbXFile.close()
        
        gdbOFile = open(gdbOFileName, 'w')
        call(args=[gdbBin, "--quiet", "--command="+gdbXFileName, binaryFileName],
             stdout=gdbOFile)
        gdbOFile.close()
        
        gdbOFile = open(gdbOFileName, 'r')
        for line in gdbOFile:
            m = re_InfoScope.match(line)
            if m is not None:
                varName = m.group("varName")
                if varName not in listLocalVarNames: 
                    continue
                else:
                    varType = m.group("varType")
                    if re.search("in register", line):
                        listLocalVarNames.remove(varName)
                    else:
                        continue
        gdbOFile.close()
        
        gdbXFile = open(gdbXFileName, 'w')
        gdbXFile.write("target sim\n")
        gdbXFile.write("load\n")
        gdbXFile.write("b %s\n" % func.functionName)
        gdbXFile.write("commands\n")
        gdbXFile.write("\tprintf \"SP = %s\\n\", %s\n" % ("%x", "$sp"))
        for varName in listLocalVarNames:
            gdbXFile.write("\tprintf \"LocalVar: %s\\n\"\n" % (varName))
            gdbXFile.write("\tprintf \"address = 0x%s\\n\", &%s\n" % ("%x", varName))
            gdbXFile.write("\tptype %s\n" % varName)
            gdbXFile.write("\tprintf \"size = %s\\n\", sizeof(%s)\n" % ("%d", varName))
#         gdbXFile.write("\tcont\n")
        gdbXFile.write("end\n")
        gdbXFile.write("run\n")
        gdbXFile.write("quit\n")
        gdbXFile.close()
        
        gdbOFile = open(gdbOFileName, 'w')
        call(args=[gdbBin, "--quiet", "--command="+gdbXFileName, binaryFileName],
             stdout=gdbOFile)
        gdbOFile.close()
        
        
        
        valSP = 0
        gdbOFile = open(gdbOFileName, 'r')
        for line in gdbOFile:
            m = re_SPLine.match(line)
            if m is not None:
                valSP = int(m.group("valSP"), 16)
                continue
            
            m = re_LocalVarLine.match(line)
            if m is not None:
                varName = m.group("varName")
                continue
            
            m = re_addressLine.match(line)
            if m is not None:
                address = int(m.group("address"), 16) - valSP 
                continue
            
            m = re_typeLine.match(line)
            if m is not None:
                varType = m.group("varType")
                continue
            
            m = re_sizeLine.match(line)
            if m is not None:
                varSize = int(m.group("varSize"))
                listLocalVariables.append(LocalVariable(varName, address, 
                                                        varType, 
                                                        varSize,
                                                        func.functionName))
                continue
        gdbOFile.close()
    
    debugPrintListLocalVariables(listLocalVariables)        
    return listLocalVariables
    
def sizeOf(type):
    if type == "unsigned int" or type == "int":
        return 4;
    elif type == "char" or type == "signed char":
        return 1;
    elif re.match("((?:\w*\s)*)\*", type):
        return 4
    