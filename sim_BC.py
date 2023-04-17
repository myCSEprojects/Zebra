from dataclasses import dataclass
from fractions import Fraction
from typing import Union, Optional, List, Dict
from lexer import Keyword, Operator, Identifier
from error import RuntimeError, typeCheckError, resolveError

# @dataclass
# class metadata:
#     '''
#     Class to store the meta data of the AST
#     '''
#     lineNumber: int
@dataclass(frozen=True)
class Variable():
    '''
    Variable class containing the name of the variable
    '''
    lineNumber: int
    name: str
    id: int
    localID: int
    def __init__(self, name):
        self.name = name
        self.id = self.localID = None

    def __repr__(self):
        return f"{self.name}::{self.id}::{self.localID}"

# Basic Data Types
@dataclass
class nil():
    pass
@dataclass
class Int():
   '''
   Class representing the integers in the language
   '''
   value: int

@dataclass
class Float():
    '''
    Floating objects represented as Fractions in python
    '''
    value: Fraction
    def __init__(self, value):
        self.value = Fraction(value)

@dataclass
class Bool():
    '''
    Seperate boolean class representing two types of values True and False
    '''
    value: bool
    @staticmethod
    def truthy(checking):
        if(checking == Int(0) or checking == Str("") or checking == Float(0) or checking == nil() or checking == Bool(False)):
            return Bool(False)
        else:
            return Bool(True)

@dataclass
class Str() :
    value: str


@dataclass
class BinOp():
    '''
    Variable evaluting to the value of the binary operation
    '''
    operator: str
    firstOperand: 'AST'
    secondOperand: 'AST'

    def implicitIntToFloat(firstOperand, secondOperand):
        '''
        Function to take of the implicit conversion of the both operands to Float if either of them is a Float
        '''
        if (isinstance(firstOperand, Float) or isinstance(secondOperand, Float)):
            if (isinstance(firstOperand, Int)):
                firstOperand = Float(firstOperand.value)
            elif (isinstance(secondOperand, Int)):
                secondOperand = Float(secondOperand.value)
        return firstOperand, secondOperand


@dataclass
class UnOp():
    '''
    Variable evaluating to the value of the unary operation 
    '''
    operator: str
    operand: 'AST'

@dataclass
class PRINT():
    print_stmt: List['AST']
    sep: Optional[str]=Str(' ')
    end: Optional[str]=Str('\n')
    
@dataclass
class Seq:
    lines: List['AST']


@dataclass
class For():
    initial : 'AST'
    condition : 'AST'
    block: 'AST'


@dataclass
class If():
    '''
    If class evaluates to Bool
    '''
    condition: 'AST'
    ifBlock: 'AST'
    elseBlock: 'AST'

@dataclass
class While():
    '''
    while loop
    '''
    condition: 'AST'
    block: 'AST'
   

# Defined binary operators in the Language
BINARY_OPERATORS = [
                    "+", "/", "-", "//", "*", "%", "^", "-",    # Binary operators for numbers
                    "<<", ">>", "&", "|",                       # Bitwise binary operators for numbers
                    "<=", "<", ">", ">=", "==", "~=",           # Binary operators for Number types(similar)
                    "&&", "||"  , "="                           # Binary operators for Booleans
]

# Defined unary operators in the language
UNARY_OPERATORS = [
                    "-", # Unary operator for numbers
                    "~"  # Unary operator for Boolean types
]

Number = Float|Int

AST = Variable|BinOp|Bool|Int|Float|If|UnOp|Str|nil|PRINT|Seq|For|While


@dataclass
class Label:
    target: int

class I:
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
    class ASSIGN:
        pass

    @dataclass
    class EQ:
        pass

    @dataclass
    class NEQ:
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
    class PRINT:
        sep: Optional[str]=Str(' ')
        end: Optional[str]=Str('\n')

    @dataclass
    class LOAD:
        localID: int

    @dataclass
    class STORE:
        localID: int

    @dataclass
    class HALT:
        pass

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
)

@dataclass
class ByteCode:
    inst: List[Instruction]

    def __init__(self):
        self.inst = []

    def label(self):
        return Label(-1)

    def emit(self, instruction):
        self.inst.append(instruction)

    def emit_label(self, label):
        label.target = len(self.inst)

class Frame:
    locals: List[AST]
    def __init__(self):
        MAX_LOCALS = 32
        self.locals = [None] * MAX_LOCALS

class VM:
    bytecode: ByteCode
    ip: int
    data: List[AST]
    currentFrame: Frame

    def load(self, bytecode):
        self.bytecode = bytecode
        self.restart()

    def restart(self):
        self.ip = 0
        self.data = []
        self.currentFrame = Frame()

    def execute(self) -> AST:
        while True:
            assert self.ip < len(self.bytecode.inst)
            match self.bytecode.inst[self.ip]:
                case I.PUSH(val):
                    self.data.append(val)
                    self.ip += 1
                case I.UMINUS():
                    op = self.data.pop()
                    if(isinstance(op, Float)):
                        self.data.append(Float(op.value * -1))
                        self.ip += 1
                    else:
                        self.data.append(Int(op.value * -1))
                        self.ip += 1
                case I.ADD():
                    secondOperand = self.data.pop()
                    firstOperand = self.data.pop()
                    if (isinstance(firstOperand, Str) and isinstance(secondOperand, Str)):
                        self.data.append(Str(firstOperand.value + secondOperand.value))
                    firstOperand, secondOperand = BinOp.implicitIntToFloat(firstOperand, secondOperand)
                    if (isinstance(firstOperand, Float)):
                        self.data.append(Float(firstOperand.value + secondOperand.value))
                        self.ip += 1
                    else:
                        self.data.append(Int(firstOperand.value + secondOperand.value))
                        self.ip += 1
                case I.SUB():
                    secondOperand = self.data.pop()
                    firstOperand = self.data.pop()
                    firstOperand, secondOperand = BinOp.implicitIntToFloat(firstOperand, secondOperand)

                    if (isinstance(firstOperand, Float)):
                        self.data.append(Float(firstOperand.value - secondOperand.value))
                        self.ip += 1
                    else:
                        self.data.append(Int(firstOperand.value - secondOperand.value))
                        self.ip += 1
                case I.MUL():
                    secondOperand = self.data.pop()
                    firstOperand = self.data.pop()

                    second_type = isinstance(secondOperand,int) or isinstance(secondOperand,Int)
                    first_type = isinstance(firstOperand,int) or isinstance(firstOperand,Int)
                    
                    if (isinstance(firstOperand,Str) and second_type):
                        self.data.append(Str(firstOperand.value * secondOperand.value))
                        self.ip += 1

                    if (first_type and isinstance(secondOperand,Str)):
                        self.data.append(Str(firstOperand.value * secondOperand.value))
                        self.ip += 1
                    
                    firstOperand, secondOperand = BinOp.implicitIntToFloat(firstOperand, secondOperand)

                    if (isinstance(firstOperand, Float)):
                        self.data.append(Float(firstOperand.value * secondOperand.value))
                        self.ip += 1
                    else:
                        self.data.append(Int(firstOperand.value * secondOperand.value))
                        self.ip += 1
                case I.DIV():
                    secondOperand = self.data.pop()
                    firstOperand = self.data.pop()
                    if (secondOperand == Int(0) or secondOperand == Float(0)):
                        RuntimeError("Cannot divide with zero")
                    self.data.append(Float(firstOperand.value/secondOperand.value))
                    self.ip += 1
                case I.EXP():
                    secondOperand = self.data.pop()
                    firstOperand = self.data.pop()
                    if isinstance(firstOperand, Int) and isinstance(secondOperand, Int):
                        self.data.append(Int(firstOperand.value ** secondOperand.value))
                        self.ip += 1
                    else:
                        self.data.append(Float(firstOperand.value ** secondOperand.value))
                        self.ip += 1
                case I.QUOT():
                    secondOperand = self.data.pop()
                    firstOperand = self.data.pop()

                    if (secondOperand == Int(0) or secondOperand == Float(0)):
                        RuntimeError("Cannot divide with zero.")
                    self.data.append(Int(int(firstOperand.value / secondOperand.value)))
                    self.ip += 1
                case I.REM():
                    secondOperand = self.data.pop()
                    firstOperand = self.data.pop()
                    self.data.append(Int(firstOperand.value % secondOperand.value))
                    self.ip += 1

                case I.LSHIFT():
                    secondOperand = self.data.pop()
                    firstOperand = self.data.pop()
                    if (secondOperand.value < 0):
                        RuntimeError(f"Negative firstOperand operand is not allowed.")
                    self.data.append(Int(firstOperand.value << secondOperand.value))
                    self.ip += 1
                case I.RSHIFT():
                    secondOperand = self.data.pop()
                    firstOperand = self.data.pop()
                    if (secondOperand.value < 0):
                        RuntimeError(f"Negative firstOperand operand not allowed.")
                    self.data.append(Int(firstOperand.value >> secondOperand.value))
                    self.ip += 1
                case I.EQ():
                    secondOperand = self.data.pop()
                    firstOperand = self.data.pop()
                    self.data.append(Bool(firstOperand.value == secondOperand.value))
                    self.ip += 1
                case I.NEQ():
                    secondOperand = self.data.pop()
                    firstOperand = self.data.pop()
                    self.data.append(Bool(firstOperand.value != secondOperand.value))
                    self.ip += 1
                case I.LT():
                    secondOperand = self.data.pop()
                    firstOperand = self.data.pop()
                    self.data.append(Bool(firstOperand.value < secondOperand.value))
                    self.ip += 1
                case I.GT():
                    secondOperand = self.data.pop()
                    firstOperand = self.data.pop()
                    self.data.append(Bool(firstOperand.value > secondOperand.value))
                    self.ip += 1
                case I.LE():
                    secondOperand = self.data.pop()
                    firstOperand = self.data.pop()
                    self.data.append(Bool(firstOperand.value <= secondOperand.value))
                    self.ip += 1
                case I.GE():
                    secondOperand = self.data.pop()
                    firstOperand = self.data.pop()
                    self.data.append(Bool(firstOperand.value >= secondOperand.value))
                    self.ip += 1
                case I.ASSIGN():
                    secondOperand = self.data.pop()
                    firstOperand = self.data.pop()
                    self.data.append(Bool(firstOperand.value >= secondOperand.value))
                    self.ip += 1
                case I.JMP(label):
                    self.ip = label.target
                case I.JMP_IF_FALSE(label):
                    op = self.data.pop()
                    if not op:
                        self.ip = label.target
                    else:
                        self.ip += 1
                case I.JMP_IF_TRUE(label):
                    op = self.data.pop()
                    if op:
                        self.ip = label.target
                    else:
                        self.ip += 1
                case I.NOT():
                    op = self.data.pop()
                    evaluated_operand = Bool.truthy(op.value)
                    self.data.append(Bool(not evaluated_operand.value))
                    self.ip += 1
                case I.DUP():
                    op = self.data.pop()
                    self.data.append(op)
                    self.data.append(op)
                    self.ip += 1
                case I.POP():
                    self.data.pop()
                    self.ip += 1
                case I.PRINT(sep, end):
                    p=self.data.pop()
                    if(sep is not None):
                        print(p.value, end=sep.value)
                    elif(end is not None):
                        print(p.value, end=end.value)
                    self.ip+=1
                case I.LOAD(localID):
                    self.data.append(self.currentFrame.locals[localID])
                    self.ip += 1
                case I.STORE(localID):
                    v = self.data.pop()
                    self.currentFrame.locals[localID] = v
                    self.ip += 1
                case I.HALT():
                    return self.data.pop()



def codegen(program: AST) -> ByteCode:
    code = ByteCode()
    generate_codegen(program, code)
    code.emit(I.HALT())
    return code

def generate_codegen (program: AST, code: ByteCode) -> None:

    def codegen_(program):
        generate_codegen(program, code)
    binary_operators = {
        "+": I.ADD(),
        "-": I.SUB(),
        "*": I.MUL(),
        "/": I.DIV(),
        "//": I.QUOT(),
        "%": I.REM(),
        "<": I.LT(),
        ">": I.GT(),
        "<=": I.LE(),
        ">=": I.GE(),
        "=": I.EQ(),
        "!=": I.NEQ(),
        "~": I.NOT(),
        ">>": I.RSHIFT(),
        "<<": I.LSHIFT(),
        "^":I.EXP(),
    }

    unary_operators={
        "-":I.UMINUS(),
        "~":I.NOT()
    }

    match program:
        case (Variable() as v) | UnOp("~", Variable() as v):
            code.emit(I.LOAD(v.localID))
        case Int(value) | Bool(value) | Str(value) | Float(value) as v:
            code.emit(I.PUSH(v))
        case nil():
            code.emit(I.PUSH(None))
        case BinOp(op, firstOperand, secondOperand) if op in binary_operators:
            codegen_(firstOperand)
            codegen_(secondOperand)
            code.emit(binary_operators[op])
        case BinOp("&&", firstOperand, secondOperand):
            E = code.label()
            codegen_(firstOperand)
            code.emit(I.DUP())
            code.emit(I.JMP_IF_FALSE(E))
            code.emit(I.POP())
            codegen_(secondOperand)
            code.emit_label(E)
        case BinOp("||", firstOperand, secondOperand):
            E = code.label()
            codegen_(firstOperand)
            code.emit(I.DUP())
            code.emit(I.JMP_IF_TRUE(E))
            code.emit(I.POP())
            codegen_(secondOperand)
            code.emit_label(E)
        case UnOp(op, operand) if op in unary_operators:
            codegen_(operand)
            code.emit(unary_operators[op])
        case Seq(lines):
            if not lines: raise RuntimeError()
            last, rest = lines[-1], lines[:-1]
            for line in rest:
                codegen_(line)
                code.emit(I.POP())
            codegen_(last)
        case If(condition, ifBlock, elseBlock):
            E = code.label()
            F = code.label()
            codegen_(condition)
            code.emit(I.JMP_IF_FALSE(F))
            codegen_(ifBlock)
            code.emit(I.JMP(E))
            code.emit_label(F)
            codegen_(elseBlock)
            code.emit_label(E)
        case While(condition, block):
            B = code.label()
            E = code.label()
            code.emit_label(B)
            codegen_(condition)
            code.emit(I.JMP_IF_FALSE(E))
            codegen_(block)
            code.emit(I.POP())
            code.emit(I.JMP(B))
            code.emit_label(E)
            code.emit(I.PUSH(None))
        case For(initial, condition, block):
            B = code.label()
            E = code.label()
            codegen_(initial)
            code.emit_label(B)
            codegen_(condition)
            code.emit(I.JMP_IF_FALSE(E))
            codegen_(block)
            code.emit(I.POP())
            code.emit(I.JMP(B))
            code.emit_label(E)
            code.emit(I.PUSH(None))

        case PRINT(print_stmt, sep, end):
            last, rest = print_stmt[-1], print_stmt[:-1]
            for stmt in (rest):
                codegen_(stmt)
                code.emit(I.PRINT(sep))
            codegen_(last)
            code.emit(I.PRINT(end))
            code.emit(I.PUSH(None))

        # Handling unknown expressions
        case _ as v:
            raise Exception(f"Got {v}, Expression|Statement Invalid")
