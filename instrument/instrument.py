import sys

class GlobalVariable:
    def __init__(self):
        self.name = ""
        self.address = 0
        self.type = ""
        self.length = -1
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
        