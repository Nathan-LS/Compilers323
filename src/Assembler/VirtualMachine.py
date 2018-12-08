from .Singleton import Singleton
from .SymbolTable import SymbolTable
import os


class VirtualMachine(metaclass=Singleton):
    def __init__(self):
        self.stack = []
        self.pc_counter = 1
        self.jump_stack = []
        self.pending_instructions = []

    def pushi(self, integer_value):
        """pushes the integer value onto the top of the stack"""
        self.stack.append(integer_value)

    def pushm(self, memory_location):
        """pushes the value stored at memory location onto TOS"""
        self.stack.append(memory_location)

    def popm(self, memory_location):
        """pops the value from the TOS and stores it at memory location"""
        SymbolTable().store_memory(memory_location, self.stack.pop())

    def stdout(self):
        """pops the value from TOS and outputs it to the standard output"""
        print(self.stack.pop())

    def stdin(self):  # todo
        """get the value from the standard input and place it onto the TOS"""
        raise NotImplementedError

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

    def jump(self, instruction_location):  # todo
        """unconditionally jump to instruction location"""
        raise NotImplementedError

    def label(self):  # todo
        """empty instruction; provides the instruction location to jump to"""
        raise NotImplementedError

    def get_pc(self)->int:
        return self.pc_counter

    def generate_instruction(self, op, oprnd):
        if oprnd == 'true':
            oprnd = 1
        elif oprnd == 'false':
            oprnd = 0
        else:
            pass
        self.pending_instructions.append({'addr': self.pc_counter, 'op': op, 'oprnd': str(oprnd)})
        self.pc_counter += 1

    def push_jumpstack(self, instr_address):
        self.jump_stack.append(instr_address)

    def back_patch(self, jump_addr):
        addr = self.jump_stack.pop()
        entry = self.pending_instructions[addr-1]
        entry['oprnd'] = jump_addr
        self.pending_instructions[addr-1] = entry

    def write_instructions(self, filename, console_print=False):
        fname = (os.path.join(os.path.dirname(filename), "instructions_{}".format(os.path.basename(filename))))  # prefix syntax to file name
        header = "{:<15} {:<16} {:<8}".format('Address', 'OP', 'Oprnd')
        with open(fname, 'w') as f:  # open file for write
            f.write(header)
            if console_print:
                print(header)
            for s in self.pending_instructions:
                instr = "{:<15} {:<16} {:<8}".format(s.get('addr'), s.get('op'), s.get('oprnd'))
                f.write(instr + '\n')
                if console_print:
                    print(instr)
            print("Wrote {} instructions to the file: ""'{}'.".format(len(self.pending_instructions) -1, fname))
