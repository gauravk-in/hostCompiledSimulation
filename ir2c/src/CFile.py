import re
import keywords
import logging

#2 April 2012 - Original function line pattern doesn't work when fn args are
# in different lines. Changing logic to check for that
#7 Octber 2012 - Wasn't recognising a function def arg list if there was a
#  comment following it on the same line. Did a fix which seems to work.
#  Not completely verified though

def readGlobalData(sourceFile,fnHash):
    """
    Reads Global Data like comments, include macros and global declarations,
    which are not included in the Blocks File.
    """
    
    f=open(sourceFile);
    line = f.readline();
    stopPrint = 0;
    comment= 0;
    fnAltArgStart = 0;
    fnName = ""
    re_ppDirective=re.compile('\s*#')
    re_commentStart = re.compile('/\*');
    re_commentEnd  = re.compile('\*/');
    re_comment = re.compile('\s*//');
    re_functionLine = re.compile('[\w\s]*\w+\s+\w+\s*\(.*\)\s*($|\{)');
    # pattern to match function with pointer return type.
    re_functionLine2 = re.compile('[\w\s]*\w+\s*\*\s*\w+\s*\(.*\)\s*($|\{)');
    re_fnLineAltStart = re.compile('[\w\s]*\w+\s+\w+\s*\([^)]*$');  # multiline fn arg list
    re_fnLineAltEnd = re.compile('.*\)\s*($|\{)');
    re_functionDesc = re.compile('.+\)')  # remove comments or '{' from function line
    re_functionName = re.compile('\w+\s*\(')
    lineNum = 0
    commentLineNum = 0
    m = None
    fnDesc_b4_Comment = 0 
    
    while line:
        lineNum = lineNum + 1
 
        
        # if not in the middle of a multiline comment and not in the middle of
        # multiline fn arg list
        if (comment == 0) and (not fnAltArgStart):
            m =re_functionLine.search(line);
            if m == None:
                m = re_fnLineAltStart.search(line)
                if m == None:
                    m = re_functionLine2.search(line);

        cM = re_commentStart.search(line)
        if cM != None:
            comment=1;
            commentLineNum = lineNum
            if m != None:
                if ( m.start() < cM.start() ):
                    fnDesc_b4_Comment = 1

        cS = re_comment.match(line)
        if cS != None:
            commentLineNum = lineNum
            if m != None:
                if ( m.start() < cS.start() ):
                    fnDesc_b4_Comment = 1

        if ( ((cS == None) and (comment == 0)) or \
                ((commentLineNum == lineNum) and (fnDesc_b4_Comment)) )\
                and (not re_ppDirective.match(line)):
            # in function params, if only "short" or "long" is mentioned,
            # replaces it with "short int" or "long int" respectively.
            line = re.sub(r'(^|\s)long(\s+)(?!(int|double))', '\g<1>long int\g<2>', line)
            line = re.sub(r'(^|\s)short(\s+)(?!(int|double))', '\g<1>short int\g<2>', line)
            m =re_functionLine.search(line);
            if m == None:
                m = re_functionLine2.search(line);
            if m and (not fnAltArgStart): 
                m=re_functionDesc.match(m.group());
                fnDesc=m.group();
                m =re_functionName.search(fnDesc);
                m = re.match('\w+',m.group());
                fnName=m.group();
                logging.debug("In main Fnmatch pattern, Fn = " + fnName)
                if fnName in fnHash: # This could be a function within ifdef, which is finally not defined
                    if not (fnName in keywords.keywords):
                        fnHash[fnName].setDesc(fnDesc);
                        logging.debug("In main Fnmatch pattern, Fn desc = " + fnDesc)
                        stopPrint = 1;

            # This is part of multiline fn arg list pattern search.
            # pushing it above the search for start of multiline arg list
            # so that it doesn't repeat the recording of the first line of the list
            if fnAltArgStart: 
                # still going through function arg list
                if fnName in fnHash: 
                    # This could be a function within ifdef,
                    # which is finally not defined, absent in Alias file
                    curFnDesc = fnHash[fnName].getDesc();
                    newDesc = curFnDesc + line;
                    fnHash[fnName].setDesc(newDesc);
          
            m = re_fnLineAltStart.search(line); 
            # main pattern doesn't match multiline function arg list
            if m and (not fnAltArgStart):      
                #This is an alternate search pattern
                fnAltArgStart = 1; 
                #function arg list starts
                m = re_functionName.search(m.group());
                m = re.match('\w+',m.group());
                fnName=m.group();
                #print"Debug. In Alt. Fnstartmatch pattern \nFn = " + fnName
                if fnName in fnHash: 
                    #This could be a function within ifdef,
                    #which is finally not defined
                    if not (fnName in keywords.keywords):
                        fnHash[fnName].setDesc(line); 
                        #add description line by line
                        #print"Debug. In Alt. Fnstartmatch pattern\nFn desc = " + fnHash[fnName].getDesc()
                        stopPrint = 1;

            m = re_fnLineAltEnd.search(line); #search for end of fn arg list
            if m and fnAltArgStart:
                fnAltArgStart = 0; #function arg list ends
                #if fnName in fnHash: #Debug
                #  print"Debug. Fn desc = " + fnHash[fnName].getDesc()

        if re_commentEnd.search(line):
            comment=0;

        fnDesc_b4_Comment = 0

        if stopPrint == 0:
            #print "Debug. Printing lines from C file"
            print line,;

        line=f.readline();

    f.close();
    return 1;

