import sys

prog_start = 0x00000000
prog_end = 0x000000FF
stack_start = 0x00000100
stack_end = 0x0000017F
data_start = 0x00010000
data_end = 0x0001007F
sp_value = 0x0000017C

invalid_memory_access = RuntimeError


def unsigned32(value):
    return value & 0xFFFFFFFF


def signed_value(value, bits):
    if value >= (1 << (bits - 1)):
        value = value - (1 << bits)
    return value


def sign_extend(value, bits):
    mask = (1 << bits) - 1
    return signed_value(value & mask, bits)


def binary32(value):
    return "0b" + format(unsigned32(value), "032b")


def create_simulator():
    simulator = {
        "reg": [0] * 32,
        "pc": prog_start,
        "prog_mem": {},
        "stack_mem": {},
        "data_mem": {},
    }
    simulator["reg"][2] = sp_value
    return simulator


def write_reg(simulator, index, value):
    if index != 0:
        simulator["reg"][index] = unsigned32(value)


def get_memory_dict(simulator, address):
    if address % 4 != 0:
        raise invalid_memory_access()
    if prog_start <= address <= prog_end:
        return simulator["prog_mem"]
    if stack_start <= address <= stack_end:
        return simulator["stack_mem"]
    if data_start <= address <= data_end:
        return simulator["data_mem"]

    raise invalid_memory_access()


def read_mem(simulator, address):
    address = unsigned32(address)
    memory = get_memory_dict(simulator, address)
    return memory.get(address, 0)


def write_mem(simulator, address, value):
    address = unsigned32(address)
    value = unsigned32(value)
    memory = get_memory_dict(simulator, address)
    memory[address] = value


def load_program(simulator, file_name):
    with open(file_name, "r") as file_obj:
        index = 0
        for raw_line in file_obj:
            line = raw_line.strip()
            if not line:
                continue
            if len(line) != 32:
                sys.exit(1)
            for char in line:
                if char not in "01":
                    sys.exit(1)
            simulator["prog_mem"][prog_start + index * 4] = int(line, 2)
            index += 1


def bits(instruction, high, low):
    size = high - low + 1
    return (instruction >> low) & ((1 << size) - 1)


def step(simulator):
    pc = simulator["pc"]
    reg = simulator["reg"]
    instruction = simulator["prog_mem"].get(pc)
    if instruction is None:
        raise invalid_memory_access()

    opcode = bits(instruction, 6, 0)
    rd = bits(instruction, 11, 7)
    funct3 = bits(instruction, 14, 12)
    rs1 = bits(instruction, 19, 15)
    rs2 = bits(instruction, 24, 20)
    funct7 = bits(instruction, 31, 25)

    next_pc = pc + 4

    u1 = reg[rs1]
    u2 = reg[rs2]
    s1 = signed_value(u1, 32)
    s2 = signed_value(u2, 32)

    if opcode == 0b0110011:
        if funct3 == 0b000:
            if funct7 == 0b0000000:
                write_reg(simulator, rd, u1 + u2)
            elif funct7 == 0b0100000:
                write_reg(simulator, rd, u1 - u2)
            else:
                raise invalid_memory_access()
        elif funct3 == 0b001:
            write_reg(simulator, rd, u1 << (u2 & 31))
        elif funct3 == 0b010:
            if s1 < s2:
                write_reg(simulator, rd, 1)
            else:
                write_reg(simulator, rd, 0)
        elif funct3 == 0b011:
            if u1 < u2:
                write_reg(simulator, rd, 1)
            else:
                write_reg(simulator, rd, 0)
        elif funct3 == 0b100:
            write_reg(simulator, rd, u1 ^ u2)
        elif funct3 == 0b101:
            write_reg(simulator, rd, u1 >> (u2 & 31))
        elif funct3 == 0b110:
            write_reg(simulator, rd, u1 | u2)
        elif funct3 == 0b111:
            write_reg(simulator, rd, u1 & u2)
        else:
            raise invalid_memory_access()

    elif opcode == 0b0010011:
        imm = sign_extend(bits(instruction, 31, 20), 12)

        if funct3 == 0b000:
            write_reg(simulator, rd, s1 + imm)
        elif funct3 == 0b011:
            if u1 < unsigned32(imm):
                write_reg(simulator, rd, 1)
            else:
                write_reg(simulator, rd, 0)
        else:
            raise invalid_memory_access()

    elif opcode == 0b0000011:
        imm = sign_extend(bits(instruction, 31, 20), 12)
        address = u1 + imm

        if funct3 == 0b010:
            write_reg(simulator, rd, read_mem(simulator, address))
        else:
            raise invalid_memory_access()

    elif opcode == 0b1100111:
        imm = sign_extend(bits(instruction, 31, 20), 12)
        target = unsigned32(u1 + imm) & ~1
        write_reg(simulator, rd, pc + 4)
        next_pc = target

    elif opcode == 0b0100011:
        imm1 = bits(instruction, 31, 25)
        imm2 = bits(instruction, 11, 7)
        imm = sign_extend((imm1 << 5) | imm2, 12)
        address = u1 + imm

        if funct3 == 0b010:
            write_mem(simulator, address, u2)
        else:
            raise invalid_memory_access()

    elif opcode == 0b1100011:
        imm = 0
        imm = imm | (bits(instruction, 31, 31) << 12)
        imm = imm | (bits(instruction, 7, 7) << 11)
        imm = imm | (bits(instruction, 30, 25) << 5)
        imm = imm | (bits(instruction, 11, 8) << 1)
        imm = sign_extend(imm, 13)

        if funct3 == 0b000 and rs1 == 0 and rs2 == 0 and imm == 0:
            return False

        take_branch = False

        if funct3 == 0b000:
            if s1 == s2:
                take_branch = True
        elif funct3 == 0b001:
            if s1 != s2:
                take_branch = True
        elif funct3 == 0b100:
            if s1 < s2:
                take_branch = True
        elif funct3 == 0b101:
            if s1 >= s2:
                take_branch = True
        elif funct3 == 0b110:
            if u1 < u2:
                take_branch = True
        elif funct3 == 0b111:
            if u1 >= u2:
                take_branch = True
        else:
            raise invalid_memory_access()

        if take_branch:
            next_pc = unsigned32(pc + imm)

    elif opcode == 0b0110111:
        imm = bits(instruction, 31, 12) << 12
        write_reg(simulator, rd, imm)

    elif opcode == 0b0010111:
        imm = bits(instruction, 31, 12) << 12
        write_reg(simulator, rd, pc + imm)

    elif opcode == 0b1101111:
        imm = 0
        imm = imm | (bits(instruction, 31, 31) << 20)
        imm = imm | (bits(instruction, 19, 12) << 12)
        imm = imm | (bits(instruction, 20, 20) << 11)
        imm = imm | (bits(instruction, 30, 21) << 1)
        imm = sign_extend(imm, 21)
        write_reg(simulator, rd, pc + 4)
        next_pc = unsigned32(pc + imm+4)

    else:
        raise invalid_memory_access()

    simulator["pc"] = unsigned32(next_pc)
    return True


def trace_line(simulator):
    items = [binary32(simulator["pc"])]
    for value in simulator["reg"]:
        items.append(binary32(value))
    return " ".join(items)


def memory_dump(simulator):
    lines = []
    for index in range(32):
        address = data_start + index * 4
        value = simulator["data_mem"].get(address, 0)
        lines.append("0x" + format(address, "08X") + ":" + binary32(value))
    return lines


def run(simulator, output_file):
    output_lines = []

    while True:
        try:
            running = step(simulator)
        except invalid_memory_access:
            break

        output_lines.append(trace_line(simulator))

        if running is False:
            output_lines = output_lines + memory_dump(simulator)
            break

    with open(output_file, "w") as file_obj:
        if len(output_lines) > 0:
            file_obj.write("\n".join(output_lines) + "\n")


def run_from_stdin():
    simulator = create_simulator()
    text = sys.stdin.read().strip()

    if text == "":
        print("Usage:")
        print("  python3 Simulator.py < input.txt")
        print("  python3 Simulator.py input.txt output.txt")
        print("  python3 Simulator.py input.txt output.txt readable_output.txt")
        sys.exit(1)

    index = 0
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if len(line) != 32:
            sys.exit(1)
        for char in line:
            if char not in "01":
                sys.exit(1)
        simulator["prog_mem"][prog_start + index * 4] = int(line, 2)
        index += 1

    while True:
        try:
            running = step(simulator)
        except invalid_memory_access:
            break

        print(trace_line(simulator))

        if running is False:
            dump = memory_dump(simulator)
            for line in dump:
                print(line)
            break


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run_from_stdin()
    elif len(sys.argv) == 3 or len(sys.argv) == 4:
        simulator = create_simulator()
        load_program(simulator, sys.argv[1])
        run(simulator, sys.argv[2])
    else:
        sys.exit(1)
