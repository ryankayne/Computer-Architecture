"""CPU functionality.""" 

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [0] * 256        # 256 bytes of memory
        self.register = [0] * 8     # 8 registers
        self.pc = 0                 # program counter
        # self.halted = False         # if halted or not (T/F)
        self.sp = 7                 # stack pointer
        self.running = True

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self, file):
        """Load a program into memory."""

        # address = 0

        # with open(file,'r') as f:
        #     all_lines = f.readlines()

        with open(file) as f:
            address = 0

            for line in f:
                line_split = line.split("#")
                num = line_split[0].strip()
                if num == "":
                    continue
                val = int(num, 2)
                self.ram[address] = val

                address += 1

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        elif op == "SUB":
            self.register[reg_a] -= self.register[reg_b]
        elif op == "MUL":
            self.register[reg_a] *= self.register[reg_b]
        elif op == "DIV":
            self.register[reg_a] /= self.register[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # Program counter, the index (address) of the current instruction
        # Reads the memory address that's stored in register

        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010

        while self.running:
        # Stores the result in "Instruction Register" from the memory (RAM) address in PC
            ir = self.ram[self.pc]
            # `LDI` instruction (EX: SAVE_REG in comp.py)
            if ir == LDI:
                address = self.ram[self.pc + 1]
                value = self.ram[self.pc + 2]
                self.register[address] = value
                self.pc += 3
            elif ir == MUL:
                self.alu("MUL", self.ram[self.pc + 1], self.ram[self.pc + 2])
                self.pc += 3
            # `PRN` instruction (EX: PRINT_REG in comp.py)
            elif ir == PRN:
                address = self.ram[self.pc + 1]
                print(self.register[address])
                self.pc += 2
            # `HLT` instruction (EX: HALT in comp.py)
            elif ir == HLT:
                self.running = False
                self.pc += 1
        # ELSE STATEMENT from comp.py
            else:
                print(f'Unknown instruction {ir} at address {self.pc}')
                break
        # self.trace()

# cpu = CPU()

# cpu.load()
# cpu.load()
# cpu.run()
