"""
Sparse word-addressable memory for the MIPS simulator.
"""


class Memory:
    def __init__(self) -> None:
        self._memory: dict[int, int] = {}

    def read(self, address: int) -> int:
        return self._memory.get(address, 0) & 0xFFFFFFFF

    def write(self, address: int, value: int) -> None:
        self._memory[address] = value & 0xFFFFFFFF

    def dump(self) -> dict[int, int]:
        return {
            address: value & 0xFFFFFFFF
            for address, value in sorted(self._memory.items())
            if (value & 0xFFFFFFFF) != 0
        }
