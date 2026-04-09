'''
Filename: MIPSSimulator/ALU.py
Description: ALU implementation for MIPS pipeline
Contributors: Samantha Hanna
'''

class ALU:
    def execute(self, opcode, operand1, operand2, imm: int = 0):
        # Perform the ALU operation based on control signals and operands
        # Return the result of the ALU operation
        result = 0

        if opcode == 'ADD' or opcode == "ADDI":
            result = operand1 + operand2
        elif opcode == 'SUB':
            result = operand1 - operand2
        elif opcode == 'MUL':
            result = operand1 * operand2
        elif opcode == 'AND':
            result = operand1 & operand2
        elif opcode == 'OR':
            result = operand1 | operand2
        elif opcode == 'SLL':
            result = operand1 << operand2
        elif opcode == 'SRL':
            result = operand1 >> operand2
        '''
        Alt implementation of ADDI:
        elif opcode == 'ADDI':
            result = operand1 + imm
        '''
        elif opcode == 'LW' or opcode == 'SW':
            result = operand1 + operand2
        elif opcode == 'BEQ':
            result = operand1 - operand2
        elif opcode == 'J':
            result = 0  # J doesn't use the ALU
        elif opcode == 'NOP':
            result = 0
        else:
            raise ValueError(f"Unknown ALU operation: {opcode}")

        result = result & 0xFFFFFFFF  # Ensures result is 32-bit
        return result