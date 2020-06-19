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
CMP = 0b10100111
JEQ = 0b01010101
JNE = 0b01010110
JMP = 0b01010100

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [0] * 256        # 256 bytes of memory
        self.register = [0] * 8     # 8 registers
        self.pc = 0                 # program counter
        self.sp = 7                 # stack pointer
        self.running = True         # if running or not (T/F)
        self.flag = 0b00000000      # set flag to default 0, compare later and change LGE at 00000LGE
        # self.flag = 0b00000111

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self, file):
        """Load a program into memory."""

        # address = 0

        # take the input file as f and open it
        with open(file) as f:
            address = 0
            
            # for every iteration/line in file,
            for line in f:
                # split the line by the # symbol
                line_split = line.split("#")
                # take the first item of the split and assign it to num (and also strip the extra spaces)
                num = line_split[0].strip()
                # if num is empty string, continue
                if num == "":
                    continue
                # turn num into a base 2 integer and assign it to value
                value = int(num, 2)
                # set the value to memory at the address (initial 0)
                self.ram[address] = value

                # increment the address to the next slot
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


    def alu(self, op, reg_a, reg_b):    # Arithmetic Logic Unit
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
        def handle_LDI(operand_a, operand_b):   # Set the value(op_b) of a register to an integer (op_a).
            # address = self.ram[self.pc + 1]
            # value = self.ram[self.pc + 2]
            self.register[operand_a] = operand_b
            self.pc += 3

        def handle_ADD(operand_a, operand_b):   # Add the value in two registers and store the result in registerA.
            # self.alu("ADD", self.ram[self.pc + 1], self.ram[self.pc + 2])
            value1 = self.register[operand_a]
            value2 = self.register[operand_b]
            self.register[operand_a] = value1 + value2
            self.pc += 3

        def handle_SUB(operand_a, operand_b):   # Subtract the value in the second register from the first, storing the result in registerA.
            # self.alu("SUB", self.ram[self.pc + 1], self.ram[self.pc + 2])
            value1 = self.register[operand_a]
            value2 = self.register[operand_b]
            self.register[operand_a] = value1 - value2
            self.pc += 3

        def handle_MUL(operand_a, operand_b):   # Multiply the values in two registers together and store the result in registerA.
            # self.alu("MUL", self.ram[self.pc + 1], self.ram[self.pc + 2])
            value1 = self.register[operand_a]
            value2 = self.register[operand_b]
            self.register[operand_a] = value1 * value2
            self.pc += 3

        def handle_DIV(operand_a, operand_b):   # Divide the value in the first register by the value in the second, storing the result in registerA.
            # self.alu("DIV", self.ram[self.pc + 1], self.ram[self.pc + 2])
            value1 = self.register[operand_a]
            value2 = self.register[operand_b]
            self.register[operand_a] = value1 / value2
            self.pc += 3

        def handle_PRN(operand_a, operand_b=None):  # Print numeric value stored in the given register. Print to the console the decimal integer value that is stored in the given register.
            # address = self.ram[self.pc + 1]
            print(self.register[operand_a])
            self.pc += 2

        def handle_PUSH(operand_a=None, operand_b=None):    # Push the value in the given register on the stack.
            register = self.ram_read(self.pc + 1)
            value = self.register[register]
            self.sp -= 1    # Decrement the SP.
            self.ram[self.sp] = value   # Copy the value in the given register to the address pointed to by SP.
            self.pc += 2

        def handle_POP(operand_a=None, operand_b=None): # Pop the value at the top of the stack into the given register.
            # if self.sp == 0xF4:
            #     return "Stack is empty."
            register = self.ram_read(self.pc + 1)
            value = self.ram[self.sp]
            self.register[register] = value # Copy the value from the address pointed to by SP to the given register.
            self.sp += 1    # Increment SP.
            self.pc += 2

        def handle_CALL(operand_a, operand_b):  # Calls a subroutine (function) at the address stored in the register.
            index_call = self.register[operand_a]   # The address of the instruction directly after CALL is pushed onto the stack.
            index_return = self.pc + 2  # The PC is set to the address stored in the given register.
            self.sp -= 1
            self.ram[self.sp] = index_return
            self.pc = index_call

        def handle_RET(operand_a, operand_b):   # Return from subroutine. Pop the value from the top of the stack and store it in the PC.
            self.pc = self.ram[self.sp]
            self.sp += 1

        def handle_CMP(operand_a, operand_b):   # Compare the values in two registers. LGE
            value1 = self.register[operand_a]
            value2 = self.register[operand_b]
            if value1 < value2:
                self.flag = 0b00000100
            if value1 > value2:
                self.flag = 0b00000010
            if value1 == value2:
                self.flag = 0b00000001
            self.pc += 3    # one op with two values

        def handle_JEQ(operand_a, operand_b):   # If equal flag is set (true), jump to the address stored in the given register.
            jump = self.register[operand_a]
            if self.flag == 0b00000001:
                self.pc = jump
            else:
                self.pc += 2    # forgot pc incrementers

        def handle_JNE(operand_a, operand_b):   # If E flag is clear (false, 0), jump to the address stored in the given register.
            jump = self.register[operand_a]
            if self.flag != 0b00000001:
                self.pc = jump
            else:
                self.pc += 2    # forgot pc incrementers

        def handle_JMP(operand_a, operand_b):   # Jump to the address stored in the given register. 
            jump = self.register[operand_a]
            self.pc = jump  # Set the PC to the address stored in the given register.

        operations = {  # quick access to all the operations via dictionary. lookup will be constant instead of O(n) now
            LDI: handle_LDI,
            ADD: handle_ADD,
            SUB: handle_SUB,
            MUL: handle_MUL,
            DIV: handle_DIV,
            PRN: handle_PRN,
            PUSH: handle_PUSH,
            POP: handle_POP,
            CALL: handle_CALL,
            RET: handle_RET,
            CMP: handle_CMP,
            JEQ: handle_JEQ,
            JNE: handle_JNE,
            JMP: handle_JMP
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
