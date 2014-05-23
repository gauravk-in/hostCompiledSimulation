# import sys
import re
import fn
import logging

def process(sourceFile, fnHash):
    """
    Reads the '.alias' file generated by the compiler frontend, to create a hash
    table of the local and global variables accessed by a function in the source
    code.
    """
    
    # Open alias file
    f=open(sourceFile + '.055t.alias');
    line = f.readline();

    # Regular Expressions
    re_fnStart = re.compile(';; Function');
    re_word = re.compile('\w+');
    re_varStart = re.compile('Referenced variables in ');
    re_varLine = re.compile('Variable:');
    re_getVar = re.compile('Variable: |, |\n');
    var_read=0;
    
    while line:
        if re_fnStart.match(line):
            m = re_word.findall(line);
            fnName = m[1];
            fnHash[fnName] = fn.Function(fnName);
            logging.debug("Function Name: " + fnName);
                        
        if var_read==1:
            if re_varLine.match(line):
                m=re_getVar.split(line);
                m[3]=re.sub(r'\{.*\}', '', m[3]);
                logging.debug("\tVariable Name: " + m[1] +", Variable Type: " + m[3]);
                fnHash[fnName].addVar(varName = m[1].strip(), varType = m[3].strip());
            elif line.strip():
                var_read=0;
                
        if re_varStart.match(line):
            var_read=1;
            
        line=f.readline();
        
    f.close();
    return 1;
    