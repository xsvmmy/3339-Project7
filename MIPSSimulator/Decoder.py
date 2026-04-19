"""
Decoder for MIPS assembly into Instruction objects.

This class reads an asm file, extracts labels, and converts each
instruction into an Instruction object that the simulator is
then able to execute.
"""

from .Instruction import Instruction, parse_register

class Decoder:
  def __init__(self, filepath: str):
    self.filepath = filepath                  # Path to asm file
    self.instructions: list[Instruction] = [] # List of decoded Instruction objects
    self.labels: dict[str, int] = {}          # Dictionary mapping label names -> PC

  def decode(self) -> list[Instruction]:
    lines = self._read_file() 

    # First Pass: Collect Labels
    pc = 0                                    # program counter for instruction index
    for line in lines:
      label, remainder = line.split(":")
      label = label.strip()

      self.labels[label] = pc                 # Store label to current address

      if not remainder.strip():
        continue

      pc += 1

    # Second Pass: Parse Instructions
    pc = 0
    for line in lines:
      if ":" in line:
        _, line = line.split(":")
        line = line.strip()                   # Remove label if applicable

        if not line:
          continue
      
      instr = self._parse_line(line, pc)
      self.instructions.append(instr.with_address(pc))  # Assign PC address
      pc += 1

    return self.instructions
  
  def _read_file(self):
    with open(self.filepath, "r") as f:
      lines = []

      for line in f:
        line = line.split("#")[0].strip()     # Remove any asm comments
        if line:
          lines.append(line)

      return lines
    
  def _parse_line(self, line: str, pc: int) -> Instruction:
    parts = line.replace(",", "").split()
    opcode = parts[0].upper()                 # Split into tokens

  #------------------------
  # NOP Instructions
  #------------------------
    if opcode == "NOP":
      return Instruction(opcode="NOP, source=line")
    
    
  #------------------------
  # R-type Instructions
  # Format : OP rd, rs, rt
  #------------------------    
    if opcode in {"ADD", "SUB", "MUL", "AND", "OR"}:
        rd = parse_register(parts[1])
        rs = parse_register(parts[2])  
        rt = parse_register(parts[3])  
        return Instruction(opcode, line, rs, rt, rd)

    # Shift instructions: OP rd, rt, shamt
    if opcode in {"SLL", "SRL"}:
        rd = parse_register(parts[1]) 
        rt = parse_register(parts[2])
        shamt = int(parts[3])  
        return Instruction(opcode, line, 0, rt, rd, shamt=shamt)

  #------------------------
  # I-type Instructions
  #------------------------
  
    # ADDI: rt = rs + immediate  
    if opcode == "ADDI":
        rt = parse_register(parts[1])
        rs = parse_register(parts[2])
        imm = int(parts[3])
        return Instruction(opcode, line, rs, rt, immediate=imm)

    # Load/Store: LW rt, offset(rs)
    if opcode in {"LW", "SW"}:
      rt = parse_register(parts[1])
      offset, reg = parts[2].split("(")
      rs = parse_register(reg.replace(")", ""))
      imm = int(offset)
      return Instruction(opcode, line, rs, rt, immediate=imm)
    
    if opcode == "BEQ":
      rs = parse_register(parts[1])
      rt = parse_register(parts[2])
      label = parts[3]
      target = self.labels[label]
      return Instruction(opcode, line, rs, rt, target=target)
    
  #------------------------
  # R-type Instructions
  #------------------------ 
    if opcode == "J":
      label = parts[1]
      target = self.labels[label]
      return Instruction(opcode, line, target=target)
    
    raise ValueError(f"Unsupported instruction: {line}")
