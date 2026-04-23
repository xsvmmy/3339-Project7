'''
Filename: MIPSSimulator/Control.py
Description: Control signal generation for MIPS instructions
Contributor: Samantha Hanna
'''

class ControlSignals:
    def __init__(self, reg_dst=False, alu_src=False, mem_to_reg=False,
                 reg_write=False, mem_read=False, mem_write=False,
                 branch=False, jump=False):
        self.reg_dst    = reg_dst
        self.alu_src    = alu_src
        self.mem_to_reg = mem_to_reg
        self.reg_write  = reg_write
        self.mem_read   = mem_read
        self.mem_write  = mem_write
        self.branch     = branch
        self.jump       = jump


def generate(opcode: str) -> ControlSignals:
    if opcode in {"ADD", "SUB", "MUL", "AND", "OR", "SLL", "SRL"}:
        return ControlSignals(reg_dst=True, reg_write=True)
    if opcode == "ADDI":
        return ControlSignals(alu_src=True, reg_write=True)
    if opcode == "LW":
        return ControlSignals(alu_src=True, mem_to_reg=True, reg_write=True, mem_read=True)
    if opcode == "SW":
        return ControlSignals(alu_src=True, mem_write=True)
    if opcode == "BEQ":
        return ControlSignals(branch=True)
    if opcode == "J":
        return ControlSignals(jump=True)
    if opcode == "NOP":
        return ControlSignals()
    raise ValueError(f"Unknown opcode: {opcode}")
