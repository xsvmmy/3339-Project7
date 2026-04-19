"""
Output formatting for MIPS simulator.

Displays pipeline state and final results.
"""

def print_cycle_state(pipeline):
    """
    Prints pipeline state for current cycle and shows which
    instruction is in each pipeline stage.
    """
    print(f"\n-----Cycle {pipeline.cycle} State-----")

    print("IF/ID :", pipeline.if_id.instruction.source)
    print("ID/EX :", pipeline.id_ex.instruction.source)
    print("EX?MEM :", pipeline.ex_mem.instruction.source)
    print("MEM/WB :", pipeline.mem_wb.instruction.source)

    print("\nRegisters: ")

    regs = pipeline.register_file.dump()                # Dump register values

    for i in range(32):
        print(f"${i:02}: {regs[i]:>10}", end=" ")
        if(i + 1) % 4 == 0:
            print()

    
def print_final_state(pipeline):
    """
    Prints final register and memory state after simulation.
    """
    print("\n-----Final Register State-----")
    regs = pipeline.register_file.dump()
    for i in range(32):
        print(f"${i:02}: {regs[i]:>10}", end=" ")
        if(i + 1) % 4 == 0:
            print()
    
    print("\n-----Final Memory State-----")
    memory = pipeline.memory.dump()
    if not memory:
        print("(empty)")
    else:
        for addr, val in memory.items():
            print(f"{addr:08x}: {val}")
