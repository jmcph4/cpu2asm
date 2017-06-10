CPU2_ISA_OP_NOP = "NOP"
CPU2_ISA_OP_MOV = "MOV"
CPU2_ISA_OP_LDL = "LDL"
CPU2_ISA_OP_ADD = "ADD"
CPU2_ISA_OP_SUB = "SUB"
CPU2_ISA_OP_MUL = "MUL"
CPU2_ISA_OP_DIV = "DIV"
CPU2_ISA_OP_MOD = "MOD"
CPU2_ISA_OP_JMP = "JMP"
CPU2_ISA_OP_JPZ = "JPZ"
CPU2_ISA_OP_JPC = "JPC"
CPU2_ISA_OP_JPV = "JPV"
CPU2_ISA_OP_JPE = "JPE"
CPU2_ISA_OP_SND = "SND"
CPU2_ISA_OP_RCV = "RCV"
CPU2_ISA_OP_RED = "RED"
CPU2_ISA_OP_WRT = "WRT"
CPU2_ISA_OP_PSH = "PSH"
CPU2_ISA_OP_POP = "POP"
CPU2_ISA_OP_LOR = "LOR"
CPU2_ISA_OP_AND = "AND"
CPU2_ISA_OP_XOR = "XOR"
CPU2_ISA_OP_NOT = "NOT"
CPU2_ISA_OP_SWP = "SWP"
CPU2_ISA_OP_CMP = "CMP"

CPU2_ISA_OPCODES = {CPU2_ISA_OP_NOP: 0x00,
                    CPU2_ISA_OP_MOV: 0x01,
                    CPU2_ISA_OP_LDL: 0x02,
                    CPU2_ISA_OP_ADD: 0x03,
                    CPU2_ISA_OP_SUB: 0x04,
                    CPU2_ISA_OP_MUL: 0x05,
                    CPU2_ISA_OP_DIV: 0x06,
                    CPU2_ISA_OP_MOD: 0x07,
                    CPU2_ISA_OP_JMP: 0x08,
                    CPU2_ISA_OP_JPZ: 0x09,
                    CPU2_ISA_OP_JPC: 0x0A,
                    CPU2_ISA_OP_JPV: 0x0B,
                    CPU2_ISA_OP_JPE: 0x0C,
                    CPU2_ISA_OP_SND: 0x0D,
                    CPU2_ISA_OP_RCV: 0x0E,
                    CPU2_ISA_OP_RED: 0x0F,
                    CPU2_ISA_OP_WRT: 0x10,
                    CPU2_ISA_OP_PSH: 0x11,
                    CPU2_ISA_OP_POP: 0x12,
                    CPU2_ISA_OP_LOR: 0x13,
                    CPU2_ISA_OP_AND: 0x14,
                    CPU2_ISA_OP_XOR: 0x15,
                    CPU2_ISA_OP_NOT: 0x16,
                    CPU2_ISA_OP_SWP: 0x17,
                    CPU2_ISA_OP_CMP: 0x18}

class Instruction(object):
    def __init__(self, opcode, dest, src, val):
        self._opcode = int(opcode)
        self._dest = int(dest)
        self._src = int(src)
        try:
            self._val = int(val)
        except ValueError:
            self._val = int(val, base=16)

    @property
    def opcode(self):
        return self._opcode

    @property
    def dest(self):
        return self._dest

    @property
    def src(self):
        return self._src

    @property
    def val(self):
        return self._val

    def __str__(self):
        s = "Instruction[opcode=" + str(self.opcode)
        s += ", dest=" + str(self.dest)
        s += ", src=" + str(self.src)
        s += ", val=" + str(self.val) + "]"

        return s

    def __bytes__(self):
        l = []

        # order of these will affect endianness
        l.append(self.val)
        l.append(self.src)
        l.append(self.dest)
        l.append(self.opcode)

        return bytes(l)

    def __repr__(self):
        return str(self.__bytes__())

class Assembler(object):
    def __init__(self, opcodes):
        self._opcodes = opcodes
    
    def parse(self, s):
        opcode = "0"
        dst = "0"
        src = "0"
        val = "0"

        if s is not None and s != "" and s.strip() != "":
            cmd = s[0:3].strip()
            op1 = s[4:s.find(",")].strip()
            op2 = s[s.find(",")+1:].strip()

            opcode = self._opcodes[cmd]

            if cmd == CPU2_ISA_OP_NOP:
                pass
            elif cmd == CPU2_ISA_OP_LDL:
                dst = op1[1:]
                val = op2
            elif cmd == CPU2_ISA_OP_PSH:
                src = op1[1:]
            elif cmd == CPU2_ISA_OP_POP:
                dst = op1[1:]
            else:
                dst = op1[1:]
                src = op2[1:]

        return Instruction(opcode, dst, src, val)

if __name__ == "__main__":
    import sys

    in_path = sys.argv[1]
    out_path = sys.argv[2]
    
    instructions = []
    asm = Assembler(CPU2_ISA_OPCODES)

    with open(in_path, "r") as f:
        for line in f:
            instructions.append(asm.parse(line))

    with open(out_path, "wb") as f:
        for i in instructions:
            f.write(bytes(i))
    
