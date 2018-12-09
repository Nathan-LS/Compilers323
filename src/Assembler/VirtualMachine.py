from .Singleton import Singleton


class VirtualMachine(metaclass=Singleton):
    def __init__(self):
        self.stack = []
        self.pc_counter = 1
        self.instructions = []
        self.memory = {}  # key: memory location, value: stored valued

    def pushi(self, integer_value):
        """pushes the integer value onto the top of the stack"""
        self.stack.append(integer_value)

    def pushm(self, memory_location):
        """pushes the value stored at memory location onto TOS"""
        self.stack.append(self.memory.get(memory_location))

    def popm(self, memory_location):
        """pops the value from the TOS and stores it at memory location"""
        self.memory[memory_location] = self.stack.pop()

    def stdout(self):
        """pops the value from TOS and outputs it to the standard output"""
        print(self.stack.pop())

    def stdin(self):
        """get the value from the standard input and place it onto the TOS"""
        self.stack.append(input())

    def add(self):
        """pop the first two items from stack and push the sum onto the TOS"""
        self.stack.append(self.stack.pop() + self.stack.pop())

    def sub(self):
        """pop the first two items from stack and push the difference onto the TOS"""
        first_val = self.stack.pop()
        second_val = self.stack.pop()
        self.stack.append(second_val - first_val)

    def mul(self):
        """pop the first two items from stack and push the product into the TOS"""
        self.stack.append(self.stack.pop() * self.stack.pop())

    def div(self):
        """pop the first two items from stack and push the result into the TOS. Ignore remainder"""
        first_val = self.stack.pop()
        second_val = self.stack.pop()
        self.stack.append(int(second_val/ first_val))

    def grt(self):
        """pops two items from the stack and pushes 1 into TOS if second item is larger otherwise push 0"""
        first_val = self.stack.pop()
        second_val = self.stack.pop()
        if second_val > first_val:
            self.stack.append(1)
        else:
            self.stack.append(0)

    def les(self):
        """pops two items from the stack and pushes 1 into TOS if second item is smaller otherwise push 0"""
        first_val = self.stack.pop()
        second_val = self.stack.pop()
        if second_val < first_val:
            self.stack.append(1)
        else:
            self.stack.append(0)

    def equ(self):
        """pops two items from the stack and pushes 1 into TOS if they are equal otherwise push 0"""
        first_val = self.stack.pop()
        second_val = self.stack.pop()
        if second_val == first_val:
            self.stack.append(1)
        else:
            self.stack.append(0)

    def neq(self):
        """pops two items from the stack and pushes 1 into TOS if they are not equal otherwise push 0"""
        first_val = self.stack.pop()
        second_val = self.stack.pop()
        if second_val != first_val:
            self.stack.append(1)
        else:
            self.stack.append(0)

    def geq(self):
        """pops two items from the stack and pushes 1 into TOS if second item is larger or equal, otherwise push 0"""
        first_val = self.stack.pop()
        second_val = self.stack.pop()
        if second_val >= first_val:
            self.stack.append(1)
        else:
            self.stack.append(0)

    def leq(self):
        """pops two items from the stack and pushes 1 into TOS if second item is less or equal, otherwise push 0"""
        first_val = self.stack.pop()
        second_val = self.stack.pop()
        if second_val <= first_val:
            self.stack.append(1)
        else:
            self.stack.append(0)

    def jumpz(self, instruction_location):
        """pop the stack and if the value is 0 then jmp to instruction location"""
        if self.stack.pop() == 0:
            self.jump(instruction_location)

    def jump(self, instruction_location):
        """unconditionally jump to instruction location"""
        self.pc_counter = instruction_location-1

    def label(self):
        """empty instruction; provides the instruction location to jump to"""
        pass

    def run_program(self, instructions: list):
        print('===== Executing Provided Assembly Instructions =====')
        self.instructions = instructions
        while self.pc_counter != len(self.instructions)+1:
            row: dict = self.instructions[self.pc_counter-1]
            instr = row.get('op')
            oprnd = row.get('oprnd')
            if instr == 'PUSHI':
                self.pushi(int(oprnd))
            elif instr == 'PUSHM':
                self.pushm(int(oprnd))
            elif instr == 'POPM':
                self.popm(int(oprnd))
            elif instr == 'STDOUT':
                self.stdout()
            elif instr == 'STDIN':
                self.stdin()
            elif instr == 'ADD':
                self.add()
            elif instr == 'SUB':
                self.sub()
            elif instr == 'MUL':
                self.mul()
            elif instr == 'DIV':
                self.div()
            elif instr == 'GRT':
                self.grt()
            elif instr == 'LES':
                self.les()
            elif instr == 'EQU':
                self.equ()
            elif instr == 'NEQ':
                self.neq()
            elif instr == 'GEQ':
                self.neq()
            elif instr == 'LEQ':
                self.leq()
            elif instr == 'JUMPZ':
                self.jumpz(int(oprnd))
            elif instr == 'JUMP':
                self.jump(int(oprnd))
            elif instr == 'LABEL':
                self.label()
            else:
                print('Invalid Instruction: {}'.format(instr))
            self.pc_counter += 1
