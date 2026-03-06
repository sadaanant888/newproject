
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
final = []
file = open("input.txt")
lines = file.readlines() 
file.close()

for line in lines:
    line = line.strip()
    if line == "":
        continue
    parts = line.split()
    other = parts[1].split(",")
    final.append([parts[0]] + other)

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

    

# ab dbddslka
