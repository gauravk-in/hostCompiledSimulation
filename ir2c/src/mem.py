import re
import fn
import keywords

TARGET_BITWIDTH = 32

UINTPTR_CAST = "(uintptr_t)"

#Zhuoran fixed the &() bug sometime before 18 Oct 2012

def memAccess(line,func):
    re_mem=re.compile('(MEM\[[^}]+})');    #MEM pattern
    re_indirection= re.compile('\*\(');
    re_invert= re.compile('~~(\w+)');
    a=re.split('(=|==|!=)',line);
    line = "";
    for i in range(len(a)):
        if i%2==1:
            line = line + a[i];
        else:          
          if re_indirection.search(a[i]):
            # Find pointer type for indirection operations
            a[i]=resolveIndirection(a[i],func.getVars());     
          m=re_mem.split(a[i]);
          a[i] = ""
	  for j in range(len(m)):
            if j%2 == 1:
		a[i] = a[i]+resolveMEM(m[j],func,a[0].strip());
            else :
                # Remove unnecessary pointer type casts
                m[j]=removePtrCast(m[j]);                         
                # Cast Ptrs where pointer arithmetic is taking place
                m[j]=resolvePtrMath(m[j],func.getPtrs());         
		a[i] = a[i] + m[j];
          # special handling for some bugs in IR operations
          line = line + re_invert.sub('\g<1> = ~\g<1>', a[i])
    return line;




def resolveMEM(mem,func,lhs):
    varHash = func.getVars()
    re_memsplit=re.compile('\w+: [^,|^\]]+');     #('\w+: [\w|\.]+')
    re_tokensplit=re.compile(': ');
    re_plus=re.compile('\+\s*(\([\w\s]+\))?');
    re_cast=re.compile('\s*\([\w\s]+\)')
    mem_components={};
    # resolve type
    m=re.search('\{.*\}',mem);
    v=re.search('[\w\.]+',m.group());
    mtype= varHash[v.group()];
    t = re.match('[ \w]+',mtype);
    mtype=t.group();
    if mtype.startswith('struct') and \
       (m.group().find('.') >= 0 or m.group().find('->') >= 0):
        # struct member access, try to get type from LHS
        m1 = re.match(r'\*\(([\w\s]+)\*\s*\)', lhs)
        m2 = re.match(r'\(([\w\s]+)\)', lhs)
        if m1:
            mtype = m1.group(1)
        elif m2:
            mtype = m2.group(1)
        elif lhs in varHash.keys():
            mtype = varHash[lhs]
        else:
            raise TypeError("Can not determine type of struct member access")
    # handle actual access
    m=re.match('[^\{]+',mem);
    m=re_memsplit.findall(m.group());
    mem="";
    plus_sign=0;
    for token in m:
       t=re_tokensplit.split(token)
       mem_components[t[0]]=t[1];
    if "symbol" in mem_components:
       mem= mem+UINTPTR_CAST+re_cast.sub('', mem_components["symbol"])
       plus_sign=1;
    if "base" in mem_components:
       if plus_sign:
          mem=mem+" + "
       mem= mem+resolvePtrMath(mem_components["base"],func.getPtrs(),1)
       plus_sign=1;
    if "index" in mem_components:
       if plus_sign: 
          mem= mem+" + ";
       mem= mem+UINTPTR_CAST+re_cast.sub('', mem_components["index"])
    if "step" in mem_components:
       step=re.match('\d+',mem_components["step"])
       mem= mem+" * "+step.group();
       plus_sign=1;
    if "offset" in mem_components:
       mem = mem + " + "
       mem_components["offset"] = mem_components["offset"].strip()
       if mem_components["offset"].isdigit():
           if int(mem_components["offset"]) >= 2**(TARGET_BITWIDTH-1):
               mem = mem + "(int)"
       mem= mem+mem_components["offset"];

    mem="*("+mtype+"*)("+mem+")"
    return mem;


def resolveIndirection(istr, varHash):
    re_1=re.compile('\*\(\([^\)]+\)')                  #Regex to get pointer cast immediately after indirection
    re_2=re.compile('\*\([\w\s]+\*')
    re_3=re.compile('\*\([\w\.]+');
    re_indirect=re.compile('\*\(');
    re_indirect2=re.compile('\*\([^\(]+\)');
    re_dataType=re.compile(' \*|\[');#('\s*[^\w]');    # Regex to remove * , [nn] etc from var Type -- e.g int[64] becomes int
    m= re_1.search(istr);
    if m:
      repl = "*"+m.group()[2:-3]+"*)(";
      istr=re_indirect.sub(repl,istr);
    else:
        m= re_2.search(istr)
        if m:
            repl = "*("+m.group()[2:-2]+"*)";
            istr=re_indirect2.sub(repl,istr);
        else:
            m=re_3.search(istr);
            a=varHash[m.group()[2:]];
            m=re_dataType.split(a,1);
            repl="*("+m[0]+"*)("
            istr=re_indirect.sub(repl,istr);
    return istr;  


def removePtrCast(str):
    re_ptrCast=re.compile('\([^\(]+ \*\)');
    str=re_ptrCast.sub("",str);
    return str;


def resolvePtrMath(str,ptrList,broad=0):
    re_var=re.compile('([\w\.]+)')      #possible variable
    re_fn=re.compile('(\w+\s*\(.*\))');      #function call ... not to be modified
    re_word=re.compile('\w+');
    m=re_fn.split(str);
    str="";
    for i in range(len(m)):
        flag=1;
        if i%2==1:
           flag=0;
           m1=re_word.match(m[i]);
           if not (m1.group() in keywords.keywords):
	       str=str+m[i];
           else:
               flag=1;
        if flag:
           if broad or (re.search('\S+\s+\S+',m[i])):
	      a=re_var.split(m[i]);
              for j in range(len(a)):
                 # constant
                 if (j%2 == 1) and a[j].isdigit():
                     # if negative, make sure it is properly sign extended
                     if int(a[j]) >= 2**(TARGET_BITWIDTH-1):
                         str = str + "(int)"
                 # ptr variable
                 elif (j%2 == 1) and a[j] in ptrList:
		     # remove address-of operator
                     addr = 0
                     cast = 1
		     re_str=re.compile('(&)')
		     strTemp=re_str.split(str);
                     if len(strTemp) > 1 and not strTemp[-1].strip():
                         addr = 1
                         str = ''.join(strTemp[:-2])
		     # remove unnecessary (and wrong) pointer type cast
                     re_str=re.compile('(\([\w\s]+\*?\s*\))')
                     strTemp=re_str.split(str)
                     if len(strTemp) > 1 and not strTemp[-1].strip():
                         if strTemp[-2].find('*') >= 0:
                             cast = 0
                         else:
                             str = ''.join(strTemp[:-2])
                     # if it was plain array access, don't cast
                     if j+1 < len(a) and a[j+1].strip().startswith('['):
                         if not addr:
                             cast = 0
                     # if it was a struct member access, don't cast
                     if j+1 < len(a) and a[j+1].strip().startswith('->'):
                         if not addr:
                             cast = 0
                     # likewise if the pointer is immediately dereferenced
                     if str.strip().endswith('*'):
                         cast = 0
                     # create properly casted pointer-taking operation
                     if cast: str = str+UINTPTR_CAST
                     if addr: str = str+"&"
                 str=str+a[j];
           else:
	      str=str+m[i];	 
    return str;




