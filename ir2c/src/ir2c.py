import sys
import re
import CFile
import BlocksFile
import fn 
import AliasFile

sourceFile = sys.argv[1];
fnHash = {};

AliasFile.process(sourceFile,fnHash);

print "/***********************************************************"
print " Intermediate representation of" 
print "    " + sourceFile
print ""
print " Converted by ir2c v0.1"
print ""
print " ***********************************************************/"
print "#include <limits.h>"
print "#include <stdint.h>"
print "#include \"ir2c.h\""
print ""
CFile.readGlobalData(sourceFile,fnHash);
BlocksFile.process(sourceFile,fnHash);
