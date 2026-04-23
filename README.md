# 3339-Project7

Proposed File Structure:

3339-Project7

— main.py                  # Parses CLI args; starting point

—MIPSSimulator

    __init__.py

    —Instruction.py       # Instruction class + binary string representation
    —Decoder.py           # reads .asm file, parses into Instruction objects

    —RegisterFile.py      # RegisterFile class
    —Memory.py            # Memory class

    —ALU.py               # ALU class
    —Control.py           # ControlSignals class + signal generation logic
    —Stages.py            # IF_ID, ID_EX, EX_MEM, MEM_WB MIPS stages
    —Pipeline.py          # Pipeline class — step(), run(), dump(), debug()

    —Output.py            # all formatting logic for dump and debug mode

—programs

    —TestInstructionsFull.asm     # demo program using every instruction
    —TestArithmetic.asm           # focused arithmetic test
    —TestMemory.asm               # focused LW/SW test

—README.md                # build and run instructions

## How to execute
python main.py --*flag*
* flag options: 
-h: Help menu
--hex: Prints hex representation of the assembly program before execution
--binary: Prints binary fields of the assembly program before execution
--debug: Prints pipeline state after each cycle

### Contributions
Samantha Hanna:
- Control.py
- Stages.py
- Pipeline.py
- Debug.py
- asm test files
- main.py

Vanny Bundick:
- Decoder.py
- RegisterFile.py
- Output.py

Amul Poudel:
- Instruction.py
- ALU.py
- Memory.py

John Parsons:
