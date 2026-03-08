
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
    

    

    


