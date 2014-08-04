#-----------------------------------------------------------------
# draw_cfg.py : This program generates the .dot file used by graphviz tool, to 
#     generate the graphs
#-----------------------------------------------------------------

import sys
import re
from optparse import OptionParser
from enum import Enum
import logging
from subprocess import call

from cfg_isc import parse_isc
from cfg_binary import parse_binary
from cfg import *

re_sourceFileName = re.compile("(\w*/)*(\w*).(\w*)")

colorUnmapped = "white"

listColorsMapped = ["aquamarine4",
                    "bisque3",
                    "blue1",
                    "brown",
                    "cadetblue",
                    "chartreuse",
                    "coral",
                    "cyan3",
                    "darkgoldenrod3",
                    "darkorchid1",
                    "darkslateblue",
                    "deeppink1",
                    "firebrick4",
                    "darkgreen",
                    "firebrick1",
                    "darkorange2",
                    "yellow",
                    "turquoise2",
                    "pink1",
                    "palegreen2",
                    "navy",
                    "maroon2",
                    "indigo",
                    "olivedrab3"]

class FileType(Enum):
    min_invalid = 0
    objdump = 1
    cSource = 2
    

def draw_cfg(function, outputPath=None):
    sourceFileName = function.fileName
    m = re_sourceFileName.match(sourceFileName)
    
    if m is not None:
        if m.group(3) == "objdump":
            fileType = FileType.objdump
            fileNamePrefix = "obj_"+m.group(2)+"_"+function.functionName
        elif m.group(3) == "c":
            fileType = FileType.cSource
            fileNamePrefix = "isc_"+m.group(2)+"_"+function.functionName
        else:
            logging.error("\t %s: File Type could not be identified." % sourceFileName)
            logging.error("File Extension must contain \"objdump\" or \"c\"")
            return -1
    else:
        logging.error("File Name could not be understood!")
        return -1
    
    if not outputPath:
        outputPath = "/tmp/"
             
    dotFileName = outputPath + fileNamePrefix + ".dot"
    psFileName = outputPath + fileNamePrefix + ".ps"
    
    dotFile = open(dotFileName, "w")
    dotFile.write("digraph "+fileNamePrefix+" {\n")
    
    i = 0
    for block in function.cfg.listBlocks:
        dotFile.write("\t")
        dotFile.write(block.name)
        if fileType == FileType.cSource:
            if block.mapsTo:
                colorName = listColorsMapped[block.mapsTo[0]]
            else:
                colorName = colorUnmapped
        elif fileType == FileType.objdump:
            colorName = listColorsMapped[i]
        else:
            colorName = colorUnmapped
        dotFile.write(" [")
        dotFile.write("fillcolor="+colorName+", style=filled")
        dotFile.write("]")
        dotFile.write(";")
        dotFile.write("\n")
        i = i + 1

    for edge in function.cfg.listEdges:
        dotFile.write("\t")
        dotFile.write(function.cfg.listBlocks[edge.fromBlockIndex].name+
                      " -> "+
                      function.cfg.listBlocks[edge.toBlockIndex].name + ";")
        dotFile.write("\n")
        
    
    for i in range(len(function.cfg.listBlocks)):
        blockAtNestingLevelFound = 0
        dotFile.write("\t{rank=same; ")
        for block in function.cfg.listBlocks:
            if block.nestingLevel == i:
                dotFile.write(block.name+" ")
                blockAtNestingLevelFound = 1
        dotFile.write("}\n")
        if blockAtNestingLevelFound == 0:
            break
        
    dotFile.write("}\n")
    dotFile.close()
    
    call(args=["dot", "-Tps", dotFileName, "-o", psFileName])
    return psFileName

def main(listInputFileNames, outputPath=None):
    listFunctions = []
    for fileName in listInputFileNames:
        m = re_sourceFileName.match(fileName)
        if m is not None:
            if m.group(3) == "objdump":
                (retListFunctions, retLineForAddress)  = parse_binary(fileName)
                listFunctions = listFunctions + retListFunctions
            elif m.group(3) == "c":
                listFunctions = listFunctions + parse_isc(fileName)
            else:
                logging.error("\t %s: File Type could not be identified." % sourceFileName)
                logging.error("File Extension must contain \"objdump\" or \"c\"")
                return -1
        else:
            logging.error("File Name could not be understood!")
            return -1
        
    for function in listFunctions:
        psFileName = draw_cfg(function, outputPath=outputPath)
        call(args=["evince", psFileName])

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    
    optparser = OptionParser()
    
    optparser.add_option("-i", "--input", action="append", dest="listInputFileNames",
                         type="string", help="Input File Name to draw CFG for",
                         metavar="FILENAME")
    
    optparser.add_option("-p", "--output_path", action="store", dest="outputPath",
                         type="string", help="Path of directory to store output files in",
                         metavar="OUTPUT_PATH")
    
    (options, args) = optparser.parse_args()
    
    if not options.listInputFileNames:
        optparser.error("Input Files not provided!")
    
    listInputFileNames = options.listInputFileNames
    outputPath = options.outputPath
    
    main(listInputFileNames, outputPath=outputPath)