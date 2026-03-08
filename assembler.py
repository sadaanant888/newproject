
registers={

    "zero":"00000",
    "ra":"00001",
    "sp":"00010",
    "gp":"00011",
    "tp":"00100",
    "t0":"00101",
    "t1":"00110",
    "t2":"00111",
    "s0":"01000",
    "fp":"01000",
    "s1":"01001",
    "a0":"01010",
    "a1":"01011",
    "a2":"01100",
    "a3":"01101",
    "a4":"01110",
    "a5":"01111",
    "a6":"10000",
    "a7":"10001",
    "s2":"10010",
    "s3":"10011",
    "s4":"10100",
    "s5":"10101",
    "s6":"10110",
    "s7":"10111",
    "s8":"11000",
    "s9":"11001",
    "s10":"11010",
    "s11":"11011",
    "t3":"11100",
    "t4":"11101",
    "t5":"11110",
    "t6":"11111"
}
final = []       # will hold instructions as nested lists
labels = {}      
pc = 0           # program counter

# Read the file
file = open("input.asm")
lines = file.readlines()
file.close()
out=open("output.txt","w")


# PASS 1: detect labels and build final nested list
for line in lines:
    line = line.strip()         
    if line == "":
        continue                

    if ":" in line:             
        parts = line.split(":", 1)
        label = parts[0].strip()    
        rest = parts[1].strip()     

        
        if label in labels:
            print("Error: duplicate label", label)
            exit()

        
        invalid = False
        if label[0] >= "0" and label[0] <= "9": 
            invalid = True
        for ch in label:  
            if not ((ch >= "a" and ch <= "z") or 
                    (ch >= "A" and ch <= "Z") or
                    (ch >= "0" and ch <= "9") or
                    ch == "_"):
                invalid = True
                break
        if invalid:
            print("Error: invalid label", label)
            exit()
        labels[label] = pc       

    
        if rest != "":
            instruction_line = rest

        else:
            continue    
    else:
        instruction_line = line     


    parts = instruction_line.split()   
    opcode = parts[0]                  
    operands = []                      

    if len(parts) > 1:                 
        operand_text = parts[1]        
        operand_parts = operand_text.split(",")   
        for op in operand_parts:     
            operands.append(op.strip())

    final.append([opcode] + operands) 
    pc = pc + 4


branch=["beq","bne","blt","bge","bltu","bgeu"]
jump=["jal"]
pc=0

# PASS-2 JUMPING OF LABEL
for q in final:
    ins=q[0]
    if(ins in branch):
        if len(q)<4:
            continue
        label=q[3]
        if label in labels:
            q[3]=labels[label]-pc
    if (ins in jump):
        label=q[2]
        if label in labels:
            q[2]=labels[label]-pc
    pc+=4
    


instruction={
    #R-type(funct7,funct3,opcode)
    "add":("0000000","000","0110011"),
    "sub":("0100000","000","0110011"),
    "sll":("0000000","001","0110011"),
    "slt":("0000000","010","0110011"),
    "sltu":("0000000","011","0110011"),
    "xor":("0000000","100","0110011"),
    "srl":("0000000","101","0110011"),
    "or":("0000000","110","0110011"),
    "and":("0000000","111","0110011"),
    #I-type(funct3,opcode)
    "lw":("010","0000011"),
    "addi":("000","0010011"),
    "sltiu":("011","0010011"),
    "jalr":("000","1100111"),
    #S-type(funct3,opcode)
    "sw":("010","0100011"),
    #B-type(funct3,opcode)
    "beq":("000","1100011"),
    "bne":("001","1100011"),
    "blt":("100","1100011"),
    "bge":("101","1100011"),
    "bltu":("110","1100011"),
    "bgeu":("111","1100011"),
    #U-type(opcode)
    "lui":("0110111",),
    "auipc":("0010111",),
    #J-type(opcode).  (20 bits imm value)
    "jal":("1101111",)
}
# REGISTER SET
register = {
"zero","ra","sp","gp","tp",
"t0","t1","t2","t3","t4","t5","t6",
"s0","s1","s2","s3","s4","s5","s6","s7",
"s8","s9","s10","s11",
"a0","a1","a2","a3","a4","a5","a6","a7"
}

# INSTRUCTION FORMAT
instructions = {
"add":3,
"sub":3,
"sll":3,
"slt":3,
"sltu":3,
"xor":3,
"srl":3,
"or":3,
"and":3,
"addi":3,
"lw":2,
"sw":2,
"beq":3,
"bne":3,
"blt":3,
"bge":3,
"jal":2,
"jalr":3
}


def is_register(reg):
    return reg in register


def valid_label(name):

    if name == "":
        return False

    if not (name[0].isalpha() or name[0] == "_"):
        return False

    for c in name:
        if not (c.isalnum() or c == "_"):
            return False

    return True


def check_imm_range(imm):

    try:
        val = int(imm)
    except:
        return False

    return -2048 <= val <= 2047



def parse_memory(op):

    if "(" not in op or ")" not in op:
        return None,None

    left = op.find("(")
    right = op.find(")")

    offset = op[:left]
    reg = op[left+1:right]

    if right != len(op)-1:
        return None,None

    return offset,reg


def detect_errors(code):

    labels = {}
    errors = []
    cleaned = []

    
    for line in code:

        if "#" in line:
            line = line.split("#")[0]

        line = line.strip()

        cleaned.append(line)

    
    for i,line in enumerate(cleaned):

        temp = line

        while ":" in temp:

            label, temp = temp.split(":",1)
            label = label.strip()

            if not valid_label(label):
                errors.append(f"Line {i+1}: Invalid label '{label}'")

            if label in labels:
                errors.append(f"Line {i+1}: Duplicate label '{label}'")

            labels[label] = i+1

            temp = temp.strip()

            if temp == "":
                break

    for i,line in enumerate(cleaned):

        if line == "":
            continue

        while ":" in line:
            line = line.split(":",1)[1].strip()

        if line == "":
            continue

        line = line.replace(","," ")

        parts = line.split()

        inst = parts[0].lower()

        if inst not in instructions:
            errors.append(f"Line {i+1}: Invalid instruction '{inst}'")
            continue

        operands = parts[1:]

        if len(operands) != instructions[inst]:
            errors.append(f"Line {i+1}: Wrong operand count for '{inst}'")
            continue

        # R TYPE 
        if inst in ["add","sub","slt"]:

            rd,rs1,rs2 = operands

            if not is_register(rd):
                errors.append(f"Line {i+1}: Invalid register '{rd}'")

            if not is_register(rs1):
                errors.append(f"Line {i+1}: Invalid register '{rs1}'")

            if not is_register(rs2):
                errors.append(f"Line {i+1}: Invalid register '{rs2}'")

        # ADDI 
        elif inst == "addi":

            rd,rs1,imm = operands

            if not is_register(rd):
                errors.append(f"Line {i+1}: Invalid register '{rd}'")

            if not is_register(rs1):
                errors.append(f"Line {i+1}: Invalid register '{rs1}'")

            if not check_imm_range(imm):
                errors.append(f"Line {i+1}: Invalid immediate '{imm}'")

        #  LOAD/STORE 
        elif inst in ["lw","sw"]:

            rd = operands[0]
            mem = operands[1]

            if not is_register(rd):
                errors.append(f"Line {i+1}: Invalid register '{rd}'")

            offset,base = parse_memory(mem)

            if offset is None:
                errors.append(f"Line {i+1}: Invalid memory format '{mem}'")

            else:

                if not check_imm_range(offset):
                    errors.append(f"Line {i+1}: Offset out of range '{offset}'")

                if not is_register(base):
                    errors.append(f"Line {i+1}: Invalid base register '{base}'")

        # BRANCH
        elif inst in ["beq","bne","blt","bge"]:
                rs1,rs2,label = operands

                if not is_register(rs1):
                    errors.append(f"Line {i+1}: Invalid register '{rs1}'")

                if not is_register(rs2):
                    errors.append(f"Line {i+1}: Invalid register '{rs2}'")

                if label.isdigit() or (label[0]=="-" and label[1:].isdigit()):
                    if not check_imm_range(label):
                        errors.append(f"Line {i+1}: Invalid immediate '{label}'")

                else:
                    if not valid_label(label):
                        errors.append(f"Line {i+1}: Invalid label '{label}'")

                    elif label not in labels:
                        errors.append(f"Line {i+1}: Undefined label '{label}'")


        #JAL
        elif inst == "jal":

            rd,label = operands

            if not is_register(rd):
                errors.append(f"Line {i+1}: Invalid register '{rd}'")

            if not valid_label(label):
                errors.append(f"Line {i+1}: Invalid label '{label}'")

            elif label not in labels:
                errors.append(f"Line {i+1}: Undefined label '{label}'")

        # JALR
        elif inst == "jalr":

            rd,rs1,imm = operands

            if not is_register(rd):
                errors.append(f"Line {i+1}: Invalid register '{rd}'")

            if not is_register(rs1):
                errors.append(f"Line {i+1}: Invalid register '{rs1}'")

            if not check_imm_range(imm):
                errors.append(f"Line {i+1}: Invalid immediate '{imm}'")

    return errors

# DRIVER 
file = open("input.asm","r")
code = file.readlines()
file.close()

errors = detect_errors(code)



if len(errors)!=0:
    for e in errors:
        out.write(e + "\n")
    out.close()
    exit()

r=["add","sub","sll","slt","sltu","xor","srl","or","and"]
i=["lw","addi","sltiu","jalr"]
s=["sw"]
b=["beq","bne","blt","bge","bltu","bgeu"]
u=["lui","auipc"]
j=["jal"]
for k in final:
    # R-TYPE
    if(k[0] in r): 
        ans=""
        if(k[0] in instruction):
            ans+=instruction[k[0]][0]
        if(k[3] in registers):
            ans+=registers[k[3]]
        if(k[2] in registers):
            ans+=registers[k[2]]
        if(k[0] in instruction):
            ans+=instruction[k[0]][1]
        if(k[1] in registers):
            ans+=registers[k[1]]
        if(k[0] in instruction):
            ans+=instruction[k[0]][2] 
    
    #I-TYPE
    if(k[0] in i):
        ans=""
        # for lw rd,imm(rs1)
        if k[0]==i[0]:
            imm=k[2]                          
            num = int(imm.split("(")[0])     
            if (num<0):
                num=num*(-1) 
                bin_imm=0                     
                x=1                     
                while(num!=0):
                    rem=num%2
                    bin_imm=bin_imm+rem*x
                    num=num//2
                    x*=10
                bin_imm=str(bin_imm)
                bin_imm=bin_imm.rjust(12,'0')

                l=[]                   
                for xy in bin_imm:                                 
                    l.append(int(xy))   
                first_1=0
                for xy in range(-1,-(len(bin_imm)+1),-1):
                    if first_1==0:
                        if l[xy]==1:
                            first_1=1
                    else:
                        if l[xy]==0:
                            l[xy]=1

                        else:
                            l[xy]=0
                complement=""
                for xy in l:
                    complement+=str(xy)                 
                
                ans+=complement
            
            else:                                
                bin_imm=0                          
                x=1                     
                while(num!=0):
                    rem=num%2
                    bin_imm=bin_imm+rem*x
                    num=num//2
                    x*=10
                bin_imm=str(bin_imm)
                bin_imm=bin_imm.rjust(12,'0')

                ans+=bin_imm

            rs1=imm.split("(")[1].split(")")[0]
            if rs1 in registers:
                ans+=registers[rs1]               
            if k[0] in instruction:
                ans+=instruction[k[0]][0]
            if k[1] in registers:
                ans+=registers[k[1]]
            if k[0] in instruction:
                ans+=instruction[k[0]][1]
            
        # except lw
        else:
            num = int(k[3])                  
            bin_imm=0                         
            x=1                      
            if (num<0):
                num=num*(-1) 
                bin_imm=0                    
                x=1                     
                while(num!=0):
                    rem=num%2
                    bin_imm=bin_imm+rem*x
                    num=num//2
                    x*=10
                bin_imm=str(bin_imm)
                bin_imm=bin_imm.rjust(12,'0')

                l=[]                   
                for xy in bin_imm:                                   
                    l.append(int(xy))   
                first_1=0
                for xy in range(-1,-(len(bin_imm)+1),-1):
                    if first_1==0:
                        if l[xy]==1:
                            first_1=1
                    else:
                        if l[xy]==0:
                            l[xy]=1

                        else:
                            l[xy]=0
                complement=""
                for xy in l:
                    complement+=str(xy)                  
                
                ans+=complement
                
            else:                                 
                bin_imm=0                          
                x=1                     
                while(num!=0):
                    rem=num%2
                    bin_imm=bin_imm+rem*x
                    num=num//2
                    x*=10
                bin_imm=str(bin_imm)
                bin_imm=bin_imm.rjust(12,'0')

                ans+=bin_imm

            if k[2] in registers:
                ans+=registers[k[2]]
            if k[0] in instruction:
                ans+=instruction[k[0]][0]
            if k[1] in registers:
                ans+=registers[k[1]]
            if k[0] in instruction:
                ans+=instruction[k[0]][1]

    # S-TYPE
    if(k[0] in s):
        ans=""
        # eg:- sw rs2,imm(rs1)
        imm=k[2]                          
        num = int(imm.split("(")[0])      
        if num<0:
            num=num*(-1)
            bin_imm=0
            x=1
            while(num!=0):
                rem=num%2
                bin_imm=bin_imm+rem*x
                num=num//2
                x*=10
            bin_imm=str(bin_imm)
            bin_imm=bin_imm.rjust(12,'0')

            l=[]                   
            for xy in bin_imm:                                   
                l.append(int(xy))   
            first_1=0
            for xy in range(-1,-(len(bin_imm)+1),-1):
                if first_1==0:
                    if l[xy]==1:
                        first_1=1
                else:
                    if l[xy]==0:
                        l[xy]=1

                    else:
                        l[xy]=0

            complement=""
            for xy in l:
                complement+=str(xy)
            
            bin_imm=complement

            imm_11_5=""                       
            y=0
            while(y<7):
                imm_11_5+=bin_imm[y]  
                y+=1
    
            imm_4_0=""                                
            y=7
            while(y<12):
                imm_4_0+=bin_imm[y]
                y+=1
            
        else:

            bin_imm=0                      
            x=1
            while(num!=0):
                rem=num%2
                bin_imm=bin_imm+rem*x
                num=num//2
                x*=10
            bin_imm=str(bin_imm)
            bin_imm=bin_imm.rjust(12,'0')

            imm_11_5=""                      
            y=0
            while(y<7):
                imm_11_5+=bin_imm[y]  
                y+=1

            imm_4_0=""                                 
            y=7
            while(y<12):
                imm_4_0+=bin_imm[y]
                y+=1

        
        
        ans+=imm_11_5                         


        if k[1] in registers:
            ans+=registers[k[1]]          

        rs1=imm.split("(")[1].split(")")[0]
        if rs1 in registers:
            ans+=registers[rs1]              
        if k[0] in instruction:
            ans+=instruction[k[0]][0]         
        
        ans+=imm_4_0                          

        if k[0] in instruction:
            ans+=instruction[k[0]][1]    
    
    # B-TYPE
    if k[0] in b:
        if len(k) < 4:
            continue
        # eg:- beq rs1,rs2, imm[12:1]
        ans=""
        num=int(k[3])                        
        bin_imm=0                         
        x=1
        if num<0:
            num=num*(-1)
            bin_imm=0
            x=1
            while(num!=0):
                rem=num%2
                bin_imm=bin_imm+rem*x
                num=num//2
                x*=10
            bin_imm=str(bin_imm)
            bin_imm=bin_imm.rjust(12,'0')

            l=[]                   
            for xy in bin_imm:                                   
                l.append(int(xy))   
            first_1=0
            for xy in range(-1,-(len(bin_imm)+1),-1):
                if first_1==0:
                    if l[xy]==1:
                        first_1=1
                else:
                    if l[xy]==0:
                        l[xy]=1

                    else:
                        l[xy]=0

            complement=""
            for xy in l:
                complement+=str(xy)

            imm_12__10_5 = complement[0] + complement[2:8]          
            imm_4_1__11 = complement[8:12] + complement[1]


        else:
            bin_imm=0
            x=1
            while(num!=0):
                rem=num%2
                bin_imm=bin_imm+rem*x
                num=num//2
                x*=10
            bin_imm=str(bin_imm)
            bin_imm=bin_imm.rjust(12,'0')

            imm_12__10_5 = bin_imm[0] + bin_imm[2:8]
            imm_4_1__11 = bin_imm[8:12] + bin_imm[1]          


        ans+=imm_12__10_5        
        
        if k[2] in registers:
            ans+=registers[k[2]]         
        if k[1] in registers:
            ans+=registers[k[1]]       
        if k[0] in instruction:
            ans+=instruction[k[0]][0]    
        
        ans+=imm_4_1__11        

        if k[0] in instruction:
            ans+=instruction[k[0]][1]  


    #U -TYPE
    if (k[0] in u): 
        ans=""
        num=int(k[2])

        temp=abs(num)

        bin_imm=""
        while(temp!=0):
            rem=temp%2
            bin_imm=str(rem)+bin_imm
            temp=temp//2

        bin_imm=bin_imm.rjust(32,'0')

        if num<0:

            l=[]
            for xy in bin_imm:
                l.append(int(xy))


            first_1=0
            for xy in range(-1,-(len(bin_imm)+1),-1):
                if first_1==0:
                    if l[xy]==1:
                        first_1=1
                else:
                    if l[xy]==0:
                        l[xy]=1
                    else:
                        l[xy]=0

    
            complement=""
            for xy in l:
                complement+=str(xy)
    
            bin_imm=complement            

        imm_31_12=""
        y=0
        while(y<20):
            imm_31_12+=bin_imm[y]
            y+=1

        ans+=imm_31_12

        if k[1] in registers:
            ans+=registers[k[1]]

        if k[0] in instruction:
            ans+=instruction[k[0]][0]


    # J-TYPE
    if k[0] in j:
        # eg:- jal rd, imm[20:1]
        ans=""
        num=int(k[2])                          
    
        if num >= 0:
            bin_imm=0
            x=1
            while(num!=0):
                rem=num%2
                bin_imm=bin_imm+rem*x
                num=num//2
                x*=10
            bin_imm=str(bin_imm)
            bin_imm=bin_imm.rjust(21,'0')
    
        else:                             
            num=num*(-1)
            bin_imm=0
            x=1
            while(num!=0):
                rem=num%2
                bin_imm=bin_imm+rem*x
                num=num//2
                x*=10
            bin_imm=str(bin_imm)
            bin_imm=bin_imm.rjust(21,'0')
    
            l=[]
            for xy in bin_imm:            
                l.append(int(xy))
            first_1=0
            for xy in range(-1,-(len(bin_imm)+1),-1):
                if first_1==0:
                    if l[xy]==1:
                        first_1=1
                else:
                    if l[xy]==0:
                        l[xy]=1
                    else:
                        l[xy]=0

            complement=""
            for xy in l:
                complement+=str(xy)

            bin_imm=complement           

        imm_20=bin_imm[-21]
        imm_10_1=bin_imm[-11:-1]
        imm_11=bin_imm[-12]
        imm_19_12=bin_imm[-20:-12]

        ans+=imm_20+imm_10_1+imm_11+imm_19_12

        if k[1] in registers:
            ans+=registers[k[1]]

        if k[0] in instruction:
            ans+=instruction[k[0]][0]
    
    out.write(ans+ "\n")
    
    


