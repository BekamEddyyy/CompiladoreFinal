.data
  var_int: .word    0:1
  var_int: .word    0:1
  var_float: .word    0:1
  var_float: .word    0:1
  var_int: .word    0:1
  var_int: .word    0:1
  var_int: .word    0:1
  var_float: .word    0:1
  var_int: .word    0:1
  var_int: .word    0:1

.text
main:
    la $t0, var_a
    lw $t0, 0($t0)
    sw $t0, var_int
    la $t0, var_b1
    lw $t0, 0($t0)
    sw $t0, var_int
    la $t0, var_a1
    lw $t0, 0($t0)
    sw $t0, var_float
    la $t0, var_ga
    lw $t0, 0($t0)
    sw $t0, var_float
    la $t0, var_b2
    lw $t0, 0($t0)
    sw $t0, var_int
    la $t0, var_c
    lw $t0, 0($t0)
    sw $t0, var_int
    la $t0, var_x
    lw $t0, 0($t0)
    sw $t0, var_int
    la $t0, var_yx
    lw $t0, 0($t0)
    sw $t0, var_float
    la $t0, var_k
    lw $t0, 0($t0)
    sw $t0, var_int
    la $t0, var_s
    lw $t0, 0($t0)
    sw $t0, var_int

