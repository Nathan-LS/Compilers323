import os
import CompilerExceptions


class InstructionGenerator(object):
    def __init__(self):
        self.pc_counter = 1
        self.jump_stack = []
        self.pending_instructions = []

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
            f.write(header + '\n')
            if console_print:
                print(header)
            for s in self.pending_instructions:
                if s.get('oprnd') == "None":
                    instr = "{:<15} {:<16}".format(s.get('addr'), s.get('op'))
                else:
                    instr = "{:<15} {:<16} {:<8}".format(s.get('addr'), s.get('op'), s.get('oprnd'))
                f.write(instr + '\n')
                if console_print:
                    print(instr)
            print("Wrote {} instructions to the file: ""'{}'.".format(len(self.pending_instructions), fname))

    def get_instructions(self)->list:
        return self.pending_instructions

    def bool_assignment_check(self, bool_identifier):
        """check if top of stack can be assigned to bool"""
        length = len(self.pending_instructions)
        if length > 0:
            val = self.pending_instructions[length-1].get('oprnd')
            if val != '1' and val != '0':
                raise CompilerExceptions.InvalidBoolAssign(bool_identifier)
        else:
            raise CompilerExceptions.InvalidBoolAssign(bool_identifier)
