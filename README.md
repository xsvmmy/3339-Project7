# 3339-Project7

## Proposed File Structure:

main.py - Parses CLI args; starting point

MIPSSimulator

    __init__.py

    — Instruction.py - Instruction class + binary string representation
    — Decoder.py - reads .asm file, parses into Instruction objects
    — RegisterFile.py - RegisterFile class
    — Memory.py - Memory class

    — ALU.py - ALU class
    — Control.py - ControlSignals class + signal generation logic
    — Stages.py - IF_ID, ID_EX, EX_MEM, MEM_WB MIPS stages
    — Pipeline.py - Pipeline class — step(), run(), dump(), debug()

    — Output.py - all formatting logic for dump and debug mode
    - Debug.py - prints state registers, control signals, state register data values, PC, and register files for each cycle

tests

    — TestInstructionsFullMain.asm - demo program using every instruction *RUN THIS TEST*
    — TestInstructionsFull.asm - another demo program using every instruction

README.md - build and run instructions

MIPS Simulator Presentation - Group 7 (1).pptx - presentation slides

## How to execute
python main.py --*flag* *file.asm*
### Flag options:

-h - Help menu

--hex - Prints hex representation of the assembly program before execution

--binary - Prints binary fields of the assembly program before execution

--debug - Prints pipeline state after each cycle

Example: python main.py --debug TestInstructionsFullMain.asm

Website link: https://project7-2-4rwq.onrender.com/
May take a while as this is free tier but you can test via website too.

## Contributions
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
