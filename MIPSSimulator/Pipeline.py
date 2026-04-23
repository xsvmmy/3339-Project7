'''
Filename: MIPSSimulator/Pipeline.py
Description: Modeling of 5-stage MIPS pipeline
    IF (Instruction Fetch)
    ID (Instruction Decode / Register Read)
    EX (Execute / ALU)
    MEM (Memory Access)
    WB (Write Back)
Contributors: Samantha Hanna
'''

from .Stages import IF_ID_Latch, ID_EX_Latch, EX_MEM_Latch, MEM_WB_Latch
from .Control import generate
from .ALU import ALU
from .Memory import Memory
from .RegisterFile import RegisterFile
from .Instruction import NOP
from . import Output
from . import Debug


class Pipeline:
    def __init__(self, instructions: list):
        self.instructions = instructions
        self.pc = 0

        self.register_file = RegisterFile()
        self.memory = Memory()
        self.alu = ALU()

        self.if_id  = IF_ID_Latch()
        self.id_ex  = ID_EX_Latch()
        self.ex_mem = EX_MEM_Latch()
        self.mem_wb = MEM_WB_Latch()

        self.cycle = 0

    def stage_IF(self) -> IF_ID_Latch:
        next_stage = IF_ID_Latch()

        if self.pc < len(self.instructions):
            next_stage.instruction = self.instructions[self.pc]
            next_stage.pc = self.pc + 1
            self.pc += 1
        else:
            next_stage.instruction = NOP
            next_stage.pc = self.pc

        return next_stage

    def stage_ID(self) -> ID_EX_Latch:
        next_latch = ID_EX_Latch()
        instr = self.if_id.instruction

        next_latch.instruction = instr
        next_latch.pc = self.if_id.pc
        next_latch.reg_rs = self.register_file.read(instr.rs)
        next_latch.reg_rt = self.register_file.read(instr.rt)
        next_latch.control = generate(instr.opcode)

        return next_latch

    def stage_EX(self) -> EX_MEM_Latch:
        next_latch = EX_MEM_Latch()
        instr = self.id_ex.instruction
        control = self.id_ex.control

        a = self.id_ex.reg_rs
        b = instr.immediate if control.alu_src else self.id_ex.reg_rt

        result, zero_flag = self.alu.execute(instr.opcode, a, b, instr.shamt)

        next_latch.instruction = instr
        next_latch.alu_result = result
        next_latch.zero_flag = zero_flag
        next_latch.reg_rt = self.id_ex.reg_rt
        next_latch.control = control

        return next_latch

    def stage_MEM(self) -> MEM_WB_Latch:
        next_latch = MEM_WB_Latch()
        instr = self.ex_mem.instruction
        control = self.ex_mem.control
        alu_result = self.ex_mem.alu_result

        mem_data = 0

        if control.mem_read:
            mem_data = self.memory.read(alu_result)

        if control.mem_write:
            self.memory.write(alu_result, self.ex_mem.reg_rt)

        if control.branch and self.ex_mem.zero_flag:
            self.pc = instr.target

        if control.jump:
            self.pc = instr.target

        next_latch.instruction = instr
        next_latch.alu_result = alu_result
        next_latch.mem_data = mem_data
        next_latch.control = control

        return next_latch

    def stage_WB(self):
        instr = self.mem_wb.instruction
        control = self.mem_wb.control

        if control.reg_write:
            dest = instr.rd if control.reg_dst else instr.rt
            value = self.mem_wb.mem_data if control.mem_to_reg else self.mem_wb.alu_result
            self.register_file.write(dest, value)

    # step function: All four stages compute their next latch values simultaneously before any latch is overwritten
    def step(self, debug: bool = False):
        self.cycle += 1
        
        next_if_id  = self.stage_IF()
        next_id_ex  = self.stage_ID()
        next_ex_mem = self.stage_EX()
        pc_before   = self.pc
        next_mem_wb = self.stage_MEM()
        self.stage_WB()

        if self.pc != pc_before:
            next_if_id  = IF_ID_Latch()
            next_id_ex  = ID_EX_Latch()
            next_ex_mem = EX_MEM_Latch()

        self.if_id  = next_if_id
        self.id_ex  = next_id_ex
        self.ex_mem = next_ex_mem
        self.mem_wb = next_mem_wb

        if debug:
            Debug.print_cycle_state(self)

    def run(self, debug: bool = False):
        while not self.is_done():
            self.step(debug=debug)

        self.dump()

    def is_done(self) -> bool:
        all_nop = (
            self.if_id.instruction.opcode  == "NOP" and
            self.id_ex.instruction.opcode  == "NOP" and
            self.ex_mem.instruction.opcode == "NOP" and
            self.mem_wb.instruction.opcode == "NOP"
        )
        return self.pc >= len(self.instructions) and all_nop

    def dump(self):
        Output.print_final_state(self)
