"""
Instruction model and helpers for the MIPS simulator.
"""

from dataclasses import dataclass, replace


REGISTER_ALIASES = {
    "zero": 0,
    "at": 1,
    "v0": 2,
    "v1": 3,
    "a0": 4,
    "a1": 5,
    "a2": 6,
    "a3": 7,
    "t0": 8,
    "t1": 9,
    "t2": 10,
    "t3": 11,
    "t4": 12,
    "t5": 13,
    "t6": 14,
    "t7": 15,
    "s0": 16,
    "s1": 17,
    "s2": 18,
    "s3": 19,
    "s4": 20,
    "s5": 21,
    "s6": 22,
    "s7": 23,
    "t8": 24,
    "t9": 25,
    "k0": 26,
    "k1": 27,
    "gp": 28,
    "sp": 29,
    "fp": 30,
    "ra": 31,
}

R_TYPE_FUNCTS = {
    "ADD": 0x20,
    "SUB": 0x22,
    "MUL": 0x18,
    "AND": 0x24,
    "OR": 0x25,
    "SLL": 0x00,
    "SRL": 0x02,
}

I_TYPE_OPCODES = {
    "ADDI": 0x08,
    "LW": 0x23,
    "SW": 0x2B,
    "BEQ": 0x04,
}

J_TYPE_OPCODES = {"J": 0x02}


@dataclass(frozen=True, slots=True)
class Instruction:
    opcode: str
    source: str = "NOP"
    rs: int = 0
    rt: int = 0
    rd: int = 0
    immediate: int = 0
    shamt: int = 0
    target: int = 0
    address: int = 0

    @property
    def binary(self) -> str:
        return encode_binary(self)

    def with_address(self, address: int) -> "Instruction":
        return replace(self, address=address)


NOP = Instruction(opcode="NOP", source="NOP")


def parse_register(token: str) -> int:
    value = token.strip().rstrip(",")
    if not value.startswith("$"):
        raise ValueError(f"Invalid register token: {token}")

    name = value[1:].lower()
    if name.isdigit():
        index = int(name)
        if 0 <= index <= 31:
            return index
        raise ValueError(f"Register out of range: {token}")

    if name in REGISTER_ALIASES:
        return REGISTER_ALIASES[name]

    raise ValueError(f"Unknown register: {token}")


def _bits(value: int, width: int) -> str:
    return format(value & ((1 << width) - 1), f"0{width}b")


def encode_binary(instruction: Instruction) -> str:
    opcode = instruction.opcode
    if opcode == "NOP":
        return "0" * 32

    if opcode in R_TYPE_FUNCTS:
        return "".join(
            [
                "000000",
                _bits(instruction.rs, 5),
                _bits(instruction.rt, 5),
                _bits(instruction.rd, 5),
                _bits(instruction.shamt, 5),
                _bits(R_TYPE_FUNCTS[opcode], 6),
            ]
        )

    if opcode in I_TYPE_OPCODES:
        immediate = instruction.immediate
        if opcode == "BEQ":
            immediate = instruction.target - (instruction.address + 1)
        return "".join(
            [
                _bits(I_TYPE_OPCODES[opcode], 6),
                _bits(instruction.rs, 5),
                _bits(instruction.rt, 5),
                _bits(immediate, 16),
            ]
        )

    if opcode in J_TYPE_OPCODES:
        return "".join([_bits(J_TYPE_OPCODES[opcode], 6), _bits(instruction.target, 26)])

    raise ValueError(f"Unsupported opcode: {opcode}")
