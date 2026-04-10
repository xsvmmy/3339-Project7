"""
Filename: MIPSSimulator/ALU.py
Description: ALU implementation for the MIPS pipeline simulator.
"""


def _mask32(value: int) -> int:
    return value & 0xFFFFFFFF


def _to_signed32(value: int) -> int:
    value = _mask32(value)
    return value if value < 0x80000000 else value - 0x100000000


class ALU:
    def execute(self, alu_op: str, operand1: int, operand2: int, shamt: int = 0) -> tuple[int, bool]:
        if alu_op in {"ADD", "ADDI", "LW", "SW"}:
            result = _to_signed32(operand1) + _to_signed32(operand2)
        elif alu_op == "SUB":
            result = _to_signed32(operand1) - _to_signed32(operand2)
        elif alu_op == "MUL":
            result = _to_signed32(operand1) * _to_signed32(operand2)
        elif alu_op == "AND":
            result = operand1 & operand2
        elif alu_op == "OR":
            result = operand1 | operand2
        elif alu_op == "SLL":
            result = _mask32(operand1) << shamt
        elif alu_op == "SRL":
            result = _mask32(operand1) >> shamt
        elif alu_op == "BEQ":
            result = _to_signed32(operand1) - _to_signed32(operand2)
        elif alu_op in {"J", "NOP"}:
            result = 0
        else:
            raise ValueError(f"Unknown ALU operation: {alu_op}")

        result = _mask32(result)
        return result, result == 0