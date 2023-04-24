from instructions import I

Instruction = (
    I.PUSH
  | I.ADD
  | I.SUB
  | I.MUL
  | I.DIV
  | I.QUOT
  | I.REM
  | I.EXP
  | I.NOT
  | I.UMINUS
  | I.JMP
  | I.JMP_IF_FALSE
  | I.JMP_IF_TRUE
  | I.DUP
  | I.POP
  | I.HALT
  | I.EQ
  | I.NEQ
  | I.LT
  | I.GT
  | I.LE
  | I.GE
  | I.LOAD
  | I.STORE
  | I.LSHIFT
  | I.RSHIFT
  | I.PRINT
  | I.APPEND
  | I.ATINDEX
  | I.SETATINDEX
  | I.PUSHFN
  | I.CALL 
  | I.RETURN
  | I.ARRAY_LEN
  | I.SLICE
  | I.ARR_REMOVE
  | I.ARR_INSERT
  | I.ARR_POP
  | I.COLL_ARR
)