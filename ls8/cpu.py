"""CPU functionality.""" 

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
ADD = 0b10100000
SUB = 0b10100001
MUL = 0b10100010
DIV = 0b10100011
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
# CMP = 0b10100111
#       00000LGE

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [0] * 256        # 256 bytes of memory
        self.register = [0] * 8     # 8 registers
        self.pc = 0                 # program counter
        self.sp = 7                 # stack pointer
        self.running = True         # if running or not (T/F)

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
                value = int(num, 2)
                self.ram[address] = value

                address += 1

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

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
        # elif op == "CMP":
        #   if self.register[reg_a] < self.register[reg_b]:
        #   
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

        # while self.running:
        #     ir = self.ram[self.pc]
        
        ## change all the self.ram pc+1 to operand_a, and self.ram pc+2 to operand_b
        def handleLDI(operand_a, operand_b):
            # address = self.ram[self.pc + 1]
            # value = self.ram[self.pc + 2]
            self.register[operand_a] = operand_b
            self.pc += 3

        def handleADD(operand_a, operand_b):
            # self.alu("ADD", self.ram[self.pc + 1], self.ram[self.pc + 2])
            value1 = self.register[operand_a]
            value2 = self.register[operand_b]
            self.register[operand_a] = value1 + value2
            self.pc += 3

        def handleSUB(operand_a, operand_b):
            # self.alu("SUB", self.ram[self.pc + 1], self.ram[self.pc + 2])
            value1 = self.register[operand_a]
            value2 = self.register[operand_b]
            self.register[operand_a] = value1 - value2
            self.pc += 3

        def handleMUL(operand_a, operand_b):
            # self.alu("MUL", self.ram[self.pc + 1], self.ram[self.pc + 2])
            value1 = self.register[operand_a]
            value2 = self.register[operand_b]
            self.register[operand_a] = value1 * value2
            self.pc += 3

        def handleDIV(operand_a, operand_b):
            # self.alu("DIV", self.ram[self.pc + 1], self.ram[self.pc + 2])
            value1 = self.register[operand_a]
            value2 = self.register[operand_b]
            self.register[operand_a] = value1 / value2
            self.pc += 3

        def handlePRN(operand_a, operand_b=None):
            # address = self.ram[self.pc + 1]
            print(self.register[operand_a])
            self.pc += 2

        def handlePUSH(operand_a=None, operand_b=None):
            register = self.ram_read(self.pc + 1)
            value = self.register[register]
            self.sp = self.sp - 1
            self.ram[self.sp] = value
            self.pc += 2

        def handlePOP(operand_a=None, operand_b=None):
            # if self.sp == 0xF4:
            #     return "Stack is empty."
            register = self.ram_read(self.pc + 1)
            value = self.ram[self.sp]
            self.register[register] = value
            self.sp += 1
            self.pc += 2

        def handleCALL(operand_a, operand_b):
            index_call = self.register[operand_a]
            index_return = self.pc + 2
            self.sp -= 1
            self.ram[self.sp] = index_return
            self.pc = index_call

        def handleRET(operand_a, operand_b):
            self.pc = self.ram[self.sp]
            self.sp += 1

        operations = {
            LDI: handleLDI,
            ADD: handleADD,
            SUB: handleSUB,
            MUL: handleMUL,
            DIV: handleDIV,
            PRN: handlePRN,
            PUSH: handlePUSH,
            POP: handlePOP,
            CALL: handleCALL,
            RET: handleRET
        }

        while True:
            ir = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if ir == HLT:
                break
            else:
                if operations[ir]:
                    operations[ir](operand_a, operand_b)
                else:
                    print(f'Unknown instruction: {ir}')
                    break


cpu = CPU()
# cpu.load()
# cpu.run()
