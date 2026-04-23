"""
Filename: MIPSSimulator/Debug.py
Description: Debug output for the MIPS pipeline simulator.
             Prints register file, state registers, and control signals each cycle.
Contributor: Samantha Hanna
"""

from .Instruction import REGISTER_ALIASES

_REGISTER_NAMES = {v: k for k, v in REGISTER_ALIASES.items()}

def _print_controls(signals):
    fields = ["reg_dst", "alu_src", "mem_to_reg", "reg_write",
              "mem_read", "mem_write", "branch", "jump"]
    print("    " + "  ".join(f"{f}={int(getattr(signals, f))}" for f in fields))

def _print_latch(name, latch, show_controls=True):
    print(f"  {name}: [{latch.instruction.source}]")
    if show_controls:
        _print_controls(latch.control)

def print_cycle_state(pipeline):
    print(f"\n===== Cycle {pipeline.cycle} =====")

    print("\n-- State Registers --")
    _print_latch("IF/ID ", pipeline.if_id,  show_controls=False)
    _print_latch("ID/EX ", pipeline.id_ex)
    _print_latch("EX/MEM", pipeline.ex_mem)
    _print_latch("MEM/WB", pipeline.mem_wb)

    print("\n-- Register File --")
    regs = pipeline.register_file.dump()
    for i in range(32):
        name = _REGISTER_NAMES.get(i, str(i))
        print(f"  ${name:<4}(${i:02}): {regs[i]:>10}", end=" ")
        if (i + 1) % 4 == 0:
            print()
