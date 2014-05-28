import sys
import re
import fn


def process(sourceFile,fnHash):
    f=open(sourceFile+ '.055t.alias');#'.t29.alias1');
    line = f.readline();
    re_fnStart=re.compile(';; Function');
    re_word=re.compile('\w+');
    re_varStart=re.compile('Referenced variables in ');
    re_varLine=re.compile('Variable:');
    re_getVar=re.compile('Variable: |, |\n');
    var_read=0
    while line:
        if re_fnStart.match(line):
            m=re_word.findall(line);
            fnName=m[1];
            fnHash[fnName]=fn.Function(fnName); 
            #print fnName;        #############debugging
        if var_read==1:
            if re_varLine.match(line):   
                m=re_getVar.split(line);
                m[3]=re.sub(r'\{.*\}', '', m[3]);
                fnHash[fnName].addVar(m[1].strip(),m[3].strip());
            elif line.strip():
                var_read=0;
        if re_varStart.match(line):
            var_read=1;
        line=f.readline();
    f.close();
    return 1;

