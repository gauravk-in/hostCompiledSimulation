import logging

class Annotation:
    def __init__(self, annotation, fileName, lineNum, replace = False):
        self.fileName = fileName
        self.lineNum = lineNum
        self.annotation = annotation
        self.replace = replace
        
    def debug(self):
        logging.debug("%s:%d: %s" % (self.fileName, self.lineNum, self.annotation))
        
def debugDictAnnot(dictAnnot):
    for lineNum in dictAnnot.iterkeys():
        for annot in dictAnnot[lineNum]:
            annot.debug()

def addAnnotationToDict(dict, lineNum, annot):
    if lineNum not in dict:
        print("adding annotation on line %d" % lineNum)
        dict[lineNum] = [annot]
    else:
        for a in dict[lineNum]:
            if a.annotation == annot.annotation and a.fileName == annot.fileName:
                return
        dict[lineNum].append(annot)