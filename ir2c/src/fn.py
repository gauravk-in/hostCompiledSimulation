import re

class Function:
  def __init__(self,name):
	self.name=name;
	self.varHash={};
        self.ptrList=[];
  def setDesc(self,desc):
	self.desc=desc;
  def getDesc(self):
	#print self.name;
	return self.desc;
  def getName(self):
	return self.name;
  def addVar(self,varName,varType):
	self.varHash[varName]=varType;
        if re.search('[\*\[]',varType):
	   self.ptrList.append(varName);
  def getVars(self):
	return self.varHash;
  def getPtrs(self):
	return self.ptrList;
  

