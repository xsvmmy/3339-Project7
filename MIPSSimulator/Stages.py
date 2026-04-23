'''
Filename: MIPSSimulator/Stages.py
Description: Defines the pipeline latches (state registers) for the 5 stages of the MIPS pipeline
- Every stage reads from the old latch and writes to a new one
- Nothing is overwritten until every stage has finished reading
Contributor: Samantha Hanna
'''

from .Control import ControlSignals
from .Instruction import NOP


class IF_ID_Latch:
    def __init__(self):
        self.reset()

    def reset(self):
        self.instruction = NOP
        self.pc = 0


class ID_EX_Latch:
    def __init__(self):
        self.reset()

    def reset(self):
        self.instruction = NOP
        self.pc = 0
        self.reg_rs = 0
        self.reg_rt = 0
        self.control = ControlSignals()


class EX_MEM_Latch:
    def __init__(self):
        self.reset()

    def reset(self):
        self.instruction = NOP
        self.pc = 0
        self.alu_result = 0
        self.zero_flag = False
        self.reg_rt = 0
        self.control = ControlSignals()


class MEM_WB_Latch:
    def __init__(self):
        self.reset()

    def reset(self):
        self.instruction = NOP
        self.pc = 0
        self.alu_result = 0
        self.mem_data = 0
        self.control = ControlSignals()
