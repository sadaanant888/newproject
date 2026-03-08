
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
labels = {}      # label -> PC address
pc = 0           # program counter

# Read the file
file = open("input.txt")
lines = file.readlines()
file.close()

# PASS 1: detect labels and build final nested list
for line in lines:
    line = line.strip()         # remove spaces
    if line == "":
        continue                # skip empty lines

    if ":" in line:             # line has a label
        parts = line.split(":", 1)
        label = parts[0].strip()    # get label name
        rest = parts[1].strip()     # instruction after label (if any)

        # Check duplicate label
        if label in labels:
            print("Error: duplicate label", label)
            exit()

        # Check invalid label (beginner style)
        invalid = False
        if label[0] >= "0" and label[0] <= "9":  # cannot start with number
            invalid = True
        for ch in label:  # only letters, numbers, underscore
            if not ((ch >= "a" and ch <= "z") or 
                    (ch >= "A" and ch <= "Z") or
                    (ch >= "0" and ch <= "9") or
                    ch == "_"):
                invalid = True
                break
        if invalid:
            print("Error: invalid label", label)
            exit()

        labels[label] = pc         # store label address

        # If instruction exists after label, process it
        if rest != "":
            instruction_line = rest

        else:
            continue    # no instruction, skip to next line

    else:
        instruction_line = line     # normal instruction without label

    # -------------------------------
    # Process the instruction into a nested list
    parts = instruction_line.split()   # split line into words
    opcode = parts[0]                  # first word is instruction
    operands = []                      # empty list for operands

    if len(parts) > 1:                 # if operands exist
        operand_text = parts[1]        # string like "x1,x2,x3"
        operand_parts = operand_text.split(",")   # split by comma
        for op in operand_parts:       # remove extra spaces
            operands.append(op.strip())

    final.append([opcode] + operands) # add as nested list
    pc = pc + 4


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
    "lui":("0110111"),
    "auipc":("0010111"),
    #J-type(opcode).  (20 bits imm value)
    "jal":("1101111")
}
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
            ans+=instruction[k[0]][0] + " "
        if(k[3] in registers):
            ans+=registers[k[3]] + " "
        if(k[2] in registers):
            ans+=registers[k[2]] + " "
        if(k[0] in instruction):
            ans+=instruction[k[0]][1] + " "
        if(k[1] in registers):
            ans+=registers[k[1]] + " "
        if(k[0] in instruction):
            ans+=instruction[k[0]][2] + "\n"
    
    #I-TYPE
    if(k[0] in i):
        ans=""
        # for lw rd,imm(rs1)
        if k[0]==i[0]:
            imm=k[2]                          ## k[2] is imm(rs1) in lw
            num = int(imm.split("(")[0])      ## num is int(imm)
            if (num<0):
                num=num*(-1) 
                bin_imm=0                     ## bin_imm will store binary of immediate.
                x=1                     
                while(num!=0):
                    rem=num%2
                    bin_imm=bin_imm+rem*x
                    num=num//2
                    x*=10
                bin_imm=str(bin_imm)
                bin_imm=bin_imm.rjust(12,'0')

                l=[]                   
                for xy in bin_imm:                                  ## 2's complement starts from here 
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
                    complement+=str(xy)                   ##complement ends  ## complement stores 2's complement of immediate
                
                ans+=complement+" "
            
            else:                                 ## for immediate>=0
                bin_imm=0                          ## bin_imm will store binary of immediate.
                x=1                     
                while(num!=0):
                    rem=num%2
                    bin_imm=bin_imm+rem*x
                    num=num//2
                    x*=10
                bin_imm=str(bin_imm)
                bin_imm=bin_imm.rjust(12,'0')

                ans+=bin_imm+ " "

            rs1=imm.split("(")[1].split(")")[0]
            if rs1 in registers:
                ans+=registers[rs1]+" "               ## ans= imm+ rs1
            if k[0] in instruction:
                ans+=instruction[k[0]][0]+" "         ## ans = imm + rs1+ funct3
            if k[1] in registers:
                ans+=registers[k[1]]+ " "                 ## ans = imm + rs1+ funct3+ rd
            if k[0] in instruction:
                ans+=instruction[k[0]][1]+ "\n"          ## ## ans = imm + rs1+ funct3+ rd+ opcode
            
        # except lw
        else:
            num = int(k[3])                   ## k[3] is imm
            bin_imm=0                         ## bin_imm will store binary of immediate. Negative immediate not handled.
            x=1                      
            if (num<0):
                num=num*(-1) 
                bin_imm=0                     ## bin_imm will store binary of immediate.
                x=1                     
                while(num!=0):
                    rem=num%2
                    bin_imm=bin_imm+rem*x
                    num=num//2
                    x*=10
                bin_imm=str(bin_imm)
                bin_imm=bin_imm.rjust(12,'0')

                l=[]                   
                for xy in bin_imm:                                  ## 2's complement starts from here 
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
                    complement+=str(xy)                   ##complement ends  ## complement stores 2's complement of immediate
                
                ans+=complement+" "                           ## ans =imm
                
            else:                                 ## for immediate>=0
                bin_imm=0                          ## bin_imm will store binary of immediate.
                x=1                     
                while(num!=0):
                    rem=num%2
                    bin_imm=bin_imm+rem*x
                    num=num//2
                    x*=10
                bin_imm=str(bin_imm)
                bin_imm=bin_imm.rjust(12,'0')

                ans+=bin_imm+ " "

            if k[2] in registers:
                ans+=registers[k[2]]+" "               ## ans= imm+ rs1
            if k[0] in instruction:
                ans+=instruction[k[0]][0]+" "         ## ans = imm + rs1+ funct3
            if k[1] in registers:
                ans+=registers[k[1]]+ " "                 ## ans = imm + rs1+ funct3+ rd
            if k[0] in instruction:
                ans+=instruction[k[0]][1]+ "\n"

    # S-TYPE
    if(k[0] in s):
        ans=""
        # eg:- sw rs2,imm(rs1)
        imm=k[2]                          ## k[2] is imm(rs1)
        num = int(imm.split("(")[0])      ## num is int(imm)
        bin_imm=0,x=1                     ## bin_imm will store binary of immediate. Negative immediate not handled. 
        while(num!=0):
            rem=num/2
            bin_imm=bin_imm+rem*x
            num=num/2
            x*=10
        bin_imm=str(bin_imm)
        bin_imm=bin_imm.rjust(12,'0')

        imm_11_5=""                       ## imm_11_5 will store imm[11:5]
        y=0
        while(y<7):
            imm_11_5+=bin_imm[y]  
            y+=1

        ans+=imm_11_5+" "                           ## ans =imm[11:5]
        if k[1] in registers:
            ans+=registers[k[1]]+ " "              ## ans = imm[11:5] + rs2

        rs1=imm.split("(")[1].split(")")[0]
        if rs1 in registers:
            ans+=registers[rs1]+" "                ## ans= imm[11:5]+ rs2+ rs1
        if k[0] in instruction:
            ans+=instruction[k[0]][0]+" "          ## ans = imm[11:5]+ rs2+ rs1+ funct3
        
        imm_4_0=""                                 ## imm_4_0 will store imm[4:0]
        y=7
        while(y<12):
            imm_4_0+=bin_imm[y]
            y+=1
        ans+=imm_4_0+" "                            ## ans = imm[11:5]+ rs2+ rs1+ funct3+ imm[4:0]

        if k[0] in instruction:
            ans+=instruction[k[0]][1]+ "\n"        ## ans = imm[11:5]+ rs2+ rs1+ funct3+ imm[4:0]+ opcode
    
    # B-TYPE
    if k[0] in b:
        # eg:- beq rs1,rs2, imm[12:1]
        ans=""
        num=k[3]                          ## k[3] is imm
        bin_imm=0,x=1                     ## bin_imm will store binary of immediate. Negative immediate not handled. 
        while(num!=0):
            rem=num/2
            bin_imm=bin_imm+rem*x
            num=num/2
            x*=10
        bin_imm=str(bin_imm)
        bin_imm=bin_imm.rjust(16,'0')

        imm_12__10_5=bin_imm[-13]+bin_imm[-11:-5]           #imm_12__10_5= imm[12|10:5]= imm[12]+imm[10:5]

        ans+=imm_12__10_5+ " "           ## ans= imm[12|10:5]
        
        if k[2] in registers:
            ans+=registers[k[2]]         ## ans= imm[12|10:5]+ rs2
        if k[1] in registers:
            ans+=registers[k[1]]         ## ans= imm[12|10:5]+ rs2 + rs1
        if k[0] in instruction:
            ans+=instruction[k[0]][0]    ## ans= imm[12|10:5]+ rs2 + rs1+ funct3
        
        imm_4_1__11=bin_imm[-5:-1]+ bin_imm[-12]    #imm_4_1__11= imm[4:1|11]= imm[4:1]+imm[11]
        ans+=imm_4_1__11+ " "            ## ans= imm[12|10:5]+ rs2 + rs1+ funct3+ imm[4:1|11]

        if k[0] in instruction:
            ans+=instruction[k[0]][1]    ## ans= imm[12|10:5]+ rs2 + rs1+ funct3+ imm[4:1|11]+ opcode
            
    # U-TYPE
    


<<<<<<< HEAD

    

<<<<<<< HEAD
    


=======
>>>>>>> 6814d6e1e7b7a8b9e755a89c138c5defdcd25646
=======
>>>>>>> dfafa04dd43c8f6902219f1f47a1730f451258f2
