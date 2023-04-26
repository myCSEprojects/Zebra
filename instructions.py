from dataclasses import dataclass
from sim import *
from typing import Optional

@dataclass
class Label:
    target: int

class I:
    @dataclass
    class SLICE:
        pass

    @dataclass
    class ARRAY_LEN:
        pass

    @dataclass
    class PUSH:
        value: AST

    @dataclass
    class UMINUS:
        pass

    @dataclass
    class ADD:
        pass

    @dataclass
    class SUB:
        pass

    @dataclass
    class MUL:
        pass

    @dataclass
    class DIV:
        pass

    @dataclass
    class QUOT:
        pass

    @dataclass
    class REM:
        pass

    @dataclass
    class EXP:
        pass

    @dataclass
    class LSHIFT:
        pass

    @dataclass
    class RSHIFT:
        pass

    @dataclass
    class EQ:
        pass

    @dataclass
    class NEQ:
        pass
    
    @dataclass
    class APPEND:
        pass

    @dataclass
    class LT:
        pass

    @dataclass
    class GT:
        pass

    @dataclass
    class LE:
        pass

    @dataclass
    class GE:
        pass

    @dataclass
    class JMP:
        label: Label

    @dataclass
    class JMP_IF_FALSE:
        label: Label


    @dataclass
    class JMP_IF_TRUE:
        label: Label

    @dataclass
    class NOT:
        pass

    @dataclass
    class DUP:
        pass

    @dataclass
    class POP:
        pass

    @dataclass
    class COLL_ARR:
        size: int
        arrayType: list
        lineNumber: int

    @dataclass
    class PRINT:
        end: Optional[str]=Str(' ')

    @dataclass
    class ASSIGN:
        localID: int
        dtype: type
        isConst: bool

    @dataclass
    class LOAD:
        localID: int
        staticJumps: int


    @dataclass
    class STORE:
        localID: int
        staticJumps: int
    
    @dataclass
    class ATINDEX:
        pass

    @dataclass
    class SETATINDEX:
        pass

    @dataclass
    class PUSHFN:
        label: Label

    @dataclass
    class CALL:
        pass

    @dataclass
    class RETURN:
        pass 

    @dataclass
    class ARR_REMOVE:
        pass

    @dataclass
    class ARR_INSERT:
        pass

    @dataclass
    class ARR_POP:
        pass

    @dataclass
    class HALT:
        pass