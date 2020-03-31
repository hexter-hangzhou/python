import os


def is_atom(s):
    if not isinstance(s, str):
        return False
    if s == "":
        return False
    return is_letter(s[0]) and all(is_letter(c) or c.isdigit() for c in s[1:])

def is_letter(s):
    return len(s) == 1 and s.lower() in "_abcdefghijklmnopqrstuvwxyz"



def loadfile(s):
    kbdict={}
    if(not os.path.isfile(s)):
        print("Error:FileNotFoundError")
        return
        print("Error:",s ,"is not a valid knowledge base")
    path = s
    with open(path, 'r', encoding='utf-8') as f:
        p=0
        values=""
        
        for line in f:
            value = line.strip() #去掉换行符
            if(len(value)==0):
                continue
            valuear=value.split()
            if(len(valuear)<3 or len(valuear)%2==0):
                print("Error:",s,"is not a valid knowledge base")
                return 
            
            if(is_atom(valuear[0]) and valuear[1]=="<--" and is_atom(valuear[2])):
                item=[]
                item.append(valuear[2])
                for i in range(3, len(valuear), 2):
                    if(is_atom(valuear[i+1]) and valuear[i]=="&"):
                        item.append(valuear[i+1])
                        continue
                    else:
                        print("Error:",s,"is not a valid knowledge base")
                        return                
            else:
                print("Error:",s,"is not a valid knowledge base")
                return           
            kbdict[valuear[0]]=item
            values=values+"\n"+value
            p+=1
        print(values.strip())
        print(p,"new rule(s) added")
        return kbdict
    
    
if __name__=="__main__":
    kbdict={}
    telllist=[]
    print("Welcome my Knowledge Base App!")
    ki = input("kb>")
    while(ki!="QQ"):
        ki=ki.strip()
        if(len(ki)>0):
            kiar=ki.split()
            if(kiar[0]=="load"):
                if(len(kiar)==2):
                    kbdict=loadfile(kiar[1])
                else:
                    print("Error: load command need filename")
            elif(kiar[0]=="tell"):
                if(len(kiar)==1):
                    print("Error: tell needs at least one atom")
                else:
                    isok= 1
                    for value in kiar[1:]:
                        if(not is_atom(value)):
                            print("Error: \""+value+"\" is not a valid atom")
                            isok =-1
                            break
                    if(isok==1):
                        for value in kiar[1:]:
                            if(value in telllist):
                                print("atom \""+ value+" already known to be true")
                                continue
                            print("\""+value+"\" added to KB")                            
                            telllist.append(value)
            elif(kiar[0]=="infer_all"):
                if(len(telllist)==0):
                    print("Error: at least one tell command is called")
                elif(len(kbdict)==0):
                    print("Error: No Rules")
                else:
                    lstlen=len(telllist)
                    inferlist=True
                    while(inferlist):
                        inferlist=False
                        for value in kbdict:
                            if(value in telllist):
                                continue
                            else:
                                rule=kbdict[value]
                                if(all((c in telllist) for c in rule)):
                                    telllist.append(value)
                                    inferlist=True
                    print("Newly inferred atoms:")
                    if(len(telllist)==lstlen):
                        print("<none>")
                    else:
                        values=telllist[lstlen]
                        for value in telllist[lstlen+1:]:
                            values=values+", "+value
                        print(values)
                    print("Atoms already known to be true:")
                    values=telllist[0]
                    for value in telllist[1:lstlen]:
                        values=values+", "+value
                    print(values)
                    
            elif(kiar[0]=="clear"): 
                telllist.clear()
                print("clear_atoms have removes all atoms")
            else:
                print("Error: unknown command \""+kiar[0]+"\"")
   
        ki = input("kb>")