import re
# import sys
# import fn
import mem

#20 Feb 2012 - modified var declaration end mark. There is no BLOCK 0.
#modified logic which sets memFlag. Earlier it wasn't getting set - Suhas
#31 Mar 2012 - added logic to preprocess block beginnings and convert
# "Block n...." to <bb n>. This is what the script was expecting and probably
#due to change in the dump format in later versions of gcc, it failed.
#Suhas
#3 Apr 2012 - re_var was matching floating point consts too. Fixed it - Suhas
#7 Oct 2012 - removed ';' when prefixing a comment symbol to tail call 
#8 Oct 2012 - added pattern 'Invalid sum of outgoing probabilities' 
#             as a line to be commented.
#8-10 Oct 2012 - removing [*_expr] sort of patterns. 

def process(sourceFile,fnHash):
    labelStart = "bb ";  # assuming that all labels names start with BB. 
                            # Change if label prefix changes - Suhas, 31 March 2012
    f=open(sourceFile+".125t.blocks");#".t99.blocks");
    line=f.readline();
    printFlag=1;
    memFlag=0;
    currentFunction="NONE";
    var_decl=[];                             #list to prevent redefinitions of variables
    declFlag=0;
    re_comments=re.compile('\s*#')                 #Lines  beginning with '#'
    re_functionStart=re.compile(';; Function');    #Start of Function
    #re_label1=re.compile('<[\s\w]+>:;');	         #Labels
    re_label1=re.compile('<[\s\w]+>:');	         #Labels
    #re_label2=re.compile('<\w+>');                 #Labels in goto statements
    re_label2=re.compile('<[\s\w]+>');                 #Labels in goto statements
    re_label3=re.compile('<.+>\s*\((<\w+>)\)');
    #re_var=re.compile('(\w+)\.(\d+)');     #For Compiler defined Variables with a '.' in them
    re_var=re.compile('([a-zA-Z]+\w*)\.(\d+)');  #For Compiler defined Variables with a '.' in them
                                                #But doesn't change floating point constants.
    re_numBytes=re.compile('(\s+-*\d+)B');
    #re_tailCall=re.compile('(\[tail call\];)');
    re_tailCall=re.compile('(\[tail call\])'); #removed ';' in regexp - Suhas, 12 Sep 2012
    re_Block=re.compile('\s*# BLOCK ');   #first occurrence marks end of variable declarations
    re_hexnum=re.compile('\s+(0[0-9a-f]+)');
    re_absExpr=re.compile('ABS_EXPR <([\w\.-]+)>');
    re_minExpr=re.compile('MIN_EXPR <([\w\.-]+), ([\w\.-]+)>');
    re_maxExpr=re.compile('MAX_EXPR <([\w\.-]+), ([\w\.-]+)>');
    re_rotrExpr=re.compile('([\w\.-]+)\s*r>>\s*([0-9]+)');
    re_rotlExpr=re.compile('([\w\.-]+)\s*r<<\s*([0-9]+)');
    re_exprToBeRemoved = re.compile('\[(rshift|lshift|plus|minus|mult|bit_and|bit_ior|bit_xor|pointer_plus)_expr\]');

    while line:
        if declFlag == 1:
            if re_Block.search(line):
                memFlag=1;
                declFlag=0;
                del var_decl[:];                      #clear this list
        if declFlag==1:
            if not (line in var_decl) :         #prevent redefinitions of variables
                var_decl.append(line);
                # replace type of pointer variables
                decl = re.split(r'([\w_.]+;)', line)
                if len(decl) == 3 and decl[0].find("unsigned") >= 0:
                    var = decl[1][:-1]
                    if var not in fnHash[currentFunction].getVars().keys() and \
                            (var.startswith("ivtmp.") or var.startswith("D.") or \
                            var.startswith("W.")):
                        line = re.split(r'\S+',decl[0])[0] + "uintptr_t " + decl[1] + decl[2]
                if len(decl) == 3 and decl[0].find('*') >= 0:
                    line = re.sub(r'\[[0-9]+\]','',decl[0]) + decl[1] + decl[2]
            else :
                printFlag=0;
        if (re_comments.match(line)):
            m = re_Block.search(line)
            if m != None:
                temp = line[m.end():]
                n = re.search('[0-9]+', temp) #search and extract basic block number
                if n != None:
                    bbNum = temp[:n.end()]
                    line = '<' + labelStart + bbNum + '>' + ':' 
                    #print "Debug!! " + line
            else:  
                line = "//" +line;
        if re.match('Invalid sum of incoming frequencies',line):
            line= "//"+ line;
        elif re.match('Invalid sum of outgoing probabilities', line):
            line = "//" + line;
        elif (re_functionStart.match(line)):
            printFlag = 0;
            m=re.search('\w+\s*\(',line);
            m=re.search('\w+',m.group());
            currentFunction = m.group();
            f.readline();
            f.readline();
            printFlag=0;
            print fnHash[currentFunction].getDesc(),;
            declFlag=1;
            memFlag=0;
        elif currentFunction != "NONE":
            line=re_numBytes.sub('\g<1>',line);
            m=re_absExpr.search(line)
            if m:
                if m.group(1) in fnHash[currentFunction].getVars().keys():
                    v_t=fnHash[currentFunction].getVars()[m.group(1)]
                    if v_t.find("long double") >= 0:
                        line=re_absExpr.sub('fabsl(\g<1>)',line)
                    elif v_t.find("double") >= 0:
                        line=re_absExpr.sub('fabs(\g<1>)',line)
                    elif v_t.find("float") >= 0:
                        line=re_absExpr.sub('fabsf(\g<1>)',line)
                    elif v_t.find("long long") >= 0:
                        line=re_absExpr.sub('llabs(\g<1>)',line)
                    elif v_t.find("long") >= 0:
                        line=re_absExpr.sub('labs(\g<1>)',line)
                    elif v_t.find("int") >= 0 or v_t.find("short") >= 0:
                        line=re_absExpr.sub('abs(\g<1>)',line)
            line=re_absExpr.sub('(\g<1>>0)?\g<1>:-\g<1>',line);
            line=re_minExpr.sub('(\g<1><\g<2>)?\g<1>:\g<2>',line);
            line=re_maxExpr.sub('(\g<1>>\g<2>)?\g<1>:\g<2>',line);
            line=re_rotrExpr.sub('(\g<1><<\g<2>)|(\g<1>>>(sizeof(\g<1>)*CHAR_BIT-\g<2>))',line);
            line=re_rotlExpr.sub('(\g<1>>>\g<2>)|(\g<1><<(sizeof(\g<1>)*CHAR_BIT-\g<2>))',line);
            line = re_exprToBeRemoved.sub('',line); #remove other types of [*_expr] tags
            if memFlag:
                line=mem.memAccess(line,fnHash[currentFunction]);
            line= re_label3.sub('\g<1>',line);
            #line1= re_label3.sub('\g<1>',line); #uncomment above line and comment these 4 not debugging
            #if line1 != line:
            #  print "Label type 3 matched"
            #  print line; #DEBUG print only
            #line = line1
            if re_label1.search(line):
                m=re.search('[\s\w]+',line);
                line =  (currentFunction+m.group()+":\n")
                line = re.sub( '\s+', '_', line,1)
                #print "Label type 1 matched"
                #print line; #DEBUG print only
            else: 
                m=re_label2.findall(line)
                for i in m :
                    m2=re.search('[\s\w]+',i)
                    subString = currentFunction+m2.group()
                    subString = re.sub( '\s+', '_', subString, 1)
                    #line = re_label2.sub(currentFunction+m2.group(),line,1)	
                    line = re_label2.sub(subString,line,1)	
                    #line1 = re_label2.sub(currentFunction+m2.group(),line,1)	
                    #if line1 == line: #if substitution did not take place
                    #  line = line1    #retain line
                    #else:             # else replace space by underscore
                    #  line = re.sub( '\s+', '_', line1,1)
                    #print "Label type 2 matched"
                    #print line; #DEBUG print only
            line=re_var.sub('\g<1>_\g<2>',line);
            line=re_tailCall.sub('//\g<1>',line);
            line=re_hexnum.sub(' 0x\g<1>',line);
        if printFlag == 1:
            print line,
        printFlag = 1;
        line = f.readline()
    return 1;
