# all_instructions.asm
#
# Exercises all 13 MIPS opcodes in a single program.
# Loads two values (10 and 5) into registers, performs arithmetic
# and logical operations on them, stores a result to memory, loads
# it back, then uses BEQ to skip over J and exit.
#
# Expected register state:
#   $t0=10  $t1=5   $t2=5
#   $t3=15  $t4=5   $t5=50
#   $t6=0   $t7=15
#   $s0=20  $s1=5   $s2=15
#
# Expected memory state:
#   mem[0] = 15

        ADDI $t0, $zero, 10
        ADDI $t1, $zero, 5
        ADDI $t2, $zero, 5
        NOP
        NOP
        ADD  $t3, $t0, $t1
        SUB  $t4, $t0, $t1
        MUL  $t5, $t0, $t1
        AND  $t6, $t0, $t1
        OR   $t7, $t0, $t1
        SLL  $s0, $t1, 2
        SRL  $s1, $t0, 1
        SW   $t3, 0($zero)
        LW   $s2, 0($zero)
        BEQ  $t1, $t2, skip
        NOP
        NOP
        NOP
        J    end
        NOP
        NOP
        NOP
skip:
        NOP
end:
        NOP
