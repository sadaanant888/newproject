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


branch=["beq","bne","blt","bge","bltu","bgeu"]
jump=["jal"]
pc=0

# PASS-2 JUMPING OF LABEL
for q in final:
    ins=q[0]
    if(ins in branch):
        label=q[3]
        if label in labels:
            q[3]=labels[label]-pc
    if (ins in jump):
        label=q[2]
        if label in labels:
            q[2]=labels[label]-pc
    pc+=4



