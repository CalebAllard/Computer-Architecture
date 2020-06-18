"""CPU functionality."""

import sys

LDI = 0b10000010 # LDI
PRN = 0b01000111 # PRN
HLT = 0b00000001 # HLT
ADD = 0b10100000 # ADD
MUL = 0b10100010 # MUL
PUSH = 0b01000101 # PUSH
POP = 0b01000110 # POP
CALL = 0b01010000 # CALL
RET = 0b00010001 # RET

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0]*256
        self.pc = 0
        self.sp = 7
        self.running = True
    ###############################################    
        self.branchtable = {
            LDI: self.ldi,
            PRN: self.prn,
            HLT: self.hlt,
            ADD: self.add,
            MUL: self.mul,
            PUSH: self.push,
            POP: self.pop,
            CALL: self.call,
            RET: self.ret



        }
    ################################################
    def ldi(self):
        self.reg[self.ram_read(self.pc + 1)] = self.ram_read(self.pc + 2)
        # self.pc += 3
    def prn(self):
        print(self.reg[self.ram_read(self.pc + 1)])
        # self.pc += 2
    def hlt(self):
        self.running = False
        # self.pc += 1
    def add(self):
        self.alu("ADD",self.ram_read(self.pc + 1), self.ram_read(self.pc + 2))
        # self.pc += 3
    def mul(self):
        self.alu("MUL",self.ram_read(self.pc + 1), self.ram_read(self.pc + 2))
        # self.pc += 3
    def push(self):
        self.sp -= 1
        reg_num = self.ram_read(self.pc + 1)
        value = self.reg[reg_num]
        top_of_stack_addr = self.reg[self.sp]
        self.ram_write(top_of_stack_addr,value)
        # self.pc += 2
    def pop(self):
        pop_item = self.ram_read(self.sp)
        reg_address = self.ram_read(self.pc + 1)
        self.reg[reg_address] = pop_item
        self.sp += 1
        # self.pc += 2
    def call(self):
        next_addr = self.pc + 2
        self.sp -= 1
        self.ram_write(self.sp,next_addr)
        address = self.reg[self.ram_read(self.pc + 1)]
        self.pc = address
    def ret(self):
        next_addr = self.ram_read(self.sp)
        self.sp += 1
        self.pc = next_addr
    #################################################
    def ram_read(self, address):
        return self.ram[address]
    
    def ram_write(self, address, value):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""
        
        address = 0

        # For now, we've just hardcoded a program:
        with open(sys.argv[1]) as f:
            
            for line in f:
                line = line.split("#")
                try:
                    v = int(line[0], 2)
                except ValueError:
                    continue
                
                self.ram_write(address, v)
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] = self.reg[reg_a] * self.reg[reg_b]

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
        
        self.reg[self.sp] = 0xf4
        
        # running = True
        
        while self.running:
            # self.trace()
            ir = self.pc
            op = self.ram[ir]
            # get op size, and pc set flag
            size = ( (op & 0b11000000) >> 6 ) + 1
            set_flag = (op & 0b00010000)
            # call opperation to be run
            self.branchtable[op]()
            
            # check to see if need to change pc
            if set_flag != 0b00010000:
                self.pc += size
            
            ##### OLD CODE ###############
            # if ir == 0b10000010: # LDI
            #     self.reg[self.ram_read(self.pc + 1)] = self.ram_read(self.pc + 2)
            #     self.pc += 3
            # elif ir == 0b01000111: # PRN
            #     print(self.reg[self.ram_read(self.pc + 1)])
            #     self.pc += 2
            # elif ir == 0b00000001: # HLT
            #     running = False
            #     self.pc += 1
            # elif ir == 0b10100000: # ADD
            #     self.alu("ADD",self.ram_read(self.pc + 1), self.ram_read(self.pc + 2))
            #     self.pc += 3
            # elif ir == 0b10100010: # MUL
            #     self.alu("MUL",self.ram_read(self.pc + 1), self.ram_read(self.pc + 2))
            #     self.pc += 3
            # elif ir == 0b01000101: # PUSH
            #     self.sp -= 1
            #     reg_num = self.ram_read(self.pc + 1)
            #     value = self.reg[reg_num]

            #     top_of_stack_addr = self.reg[self.sp]
            #     self.ram_write(top_of_stack_addr,value)
            #     self.pc += 2
            # elif ir == 0b01000110: # POP
            #     pop_item = self.ram_read(self.sp)
            #     reg_address = self.ram_read(self.pc + 1)
            #     self.reg[reg_address] = pop_item
            #     self.sp += 1
            #     self.pc += 2
            # elif ir == 0b01010000: # CALL
            #     next_addr = self.pc + 2
            #     self.sp -= 1
            #     self.ram_write(self.sp,next_addr)
            #     address = self.reg[self.ram_read(self.pc + 1)]
            #     self.pc = address
            # elif ir == 0b00010001: # RET
            #     next_addr = self.ram_read(self.sp)
            #     self.sp += 1
            #     self.pc = next_addr
            # else:
            #     sys.exit(1)
                

