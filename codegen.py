from dataclasses import dataclass
from fractions import Fraction
from typing import Union, Optional, List, Dict
from lexer import Keyword, Operator, Identifier
from error import RuntimeError, typeCheckError, resolveError
from sim import *
from sim import Variable, nil, Int, Float, Bool, Str, BinOp, UnOp, PRINT, Seq, For,If, While, Declare, zArray, Block, array_append, array_insert, array_len, array_pop, array_remove, AtIndex, SetAtIndex, FnObject, Slice
from instruction_list import Instruction    # The instructions list
from instructions import I, Label           # The instruction class

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
class CompiledFunction:
    entry: int
    staticLink: 'Frame'

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

def codegen(program: AST) -> ByteCode:
    code = ByteCode()
    generate_codegen(program, code)
    code.emit(I.HALT())
    return code

# List of supported binary operations
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
    "==": I.EQ(),
    "!=": I.NEQ(),
    "~": I.NOT(),
    ">>": I.RSHIFT(),
    "<<": I.LSHIFT(),
    "^":I.EXP(),
}

# List of supported unary operations
unary_operators={
    "-":I.UMINUS(),
    "~":I.NOT()
}

# CODE GENERATION
def generate_codegen (program: AST, code: ByteCode) -> None:

    def codegen_(program):
        generate_codegen(program, code)

    match program:
        
        case (Variable() as v) | UnOp("~", Variable() as v):
            code.emit(I.LOAD(v.localID, v.staticJumps))
        
        case Int(value) | Bool(value) | Str(value) | Float(value) as v:
            code.emit(I.PUSH(v))
        
        case zArray() as arr:
            for i in arr.elements:
                codegen_(i)

            code.emit(I.COLL_ARR(len(arr.elements), arr.dtype, arr.lineNumber))
        
        case nil():
            code.emit(I.PUSH(nil()))
        
        case BinOp(lineNumber, op, firstOperand, secondOperand) if op in binary_operators:
            codegen_(firstOperand)
            codegen_(secondOperand)
            code.emit(binary_operators[op])
        
        case BinOp(lineNumber, "&&", firstOperand, secondOperand):
            E = code.label()
            codegen_(firstOperand)
            code.emit(I.DUP())
            code.emit(I.JMP_IF_FALSE(E))
            code.emit(I.POP())
            codegen_(secondOperand)
            code.emit_label(E)
        
        case BinOp(lineNumber, "||", firstOperand, secondOperand):
            E = code.label()
            codegen_(firstOperand)
            code.emit(I.DUP())
            code.emit(I.JMP_IF_TRUE(E))
            code.emit(I.POP())
            codegen_(secondOperand)
            code.emit_label(E)
        
        case BinOp(lineNumber, "=", firstOperand, secondOperand):
            codegen_(secondOperand)
            code.emit(I.STORE(firstOperand.localID, firstOperand.staticJumps))
            code.emit(I.PUSH(nil()))

        case Block(blockStatements):
            codegen_(blockStatements)
            
        case UnOp(lineNumber, op, operand) if op in unary_operators:
            codegen_(operand)
            code.emit(unary_operators[op])
        
        case Seq(lines):
            if len(lines) == 0:
                code.emit(I.PUSH(nil()))
            elif len(lines) == 1:
                codegen_(lines[0])
            else:
                last, rest = lines[-1], lines[:-1]
                for line in rest:
                    codegen_(line)
                    code.emit(I.POP())
                codegen_(last)
        
        case If(lineNumber, condition, ifBlock, elseBlock):
            E = code.label()
            F = code.label()
            codegen_(condition)
            code.emit(I.JMP_IF_FALSE(F))
            codegen_(ifBlock)
            code.emit(I.JMP(E))
            code.emit_label(F)
            codegen_(elseBlock)
            code.emit_label(E)
        
        case While(lineNumber, condition, block):
            B = code.label()
            E = code.label()
            code.emit_label(B)
            codegen_(condition)
            code.emit(I.JMP_IF_FALSE(E))
            codegen_(block)
            code.emit(I.POP())
            code.emit(I.JMP(B))
            code.emit_label(E)
            code.emit(I.PUSH(nil()))
        
        case For(lineNumber, initial, condition, block):
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
            code.emit(I.PUSH(nil()))

        case PRINT(lineNumber, print_stmt, sep, end):
            if len(print_stmt) == 0:
                code.emit(I.PRINT(end.value))
                code.emit(I.PUSH(nil()))
                return
            last, rest = print_stmt[-1], print_stmt[:-1]
            for stmt in (rest):
                codegen_(stmt)
                code.emit(I.PRINT(sep.value))
            codegen_(last)
            code.emit(I.PRINT(end.value))
            code.emit(I.PUSH(nil()))

        case Declare(lineNumber, var, value, dtype, isConst):
            codegen_(value)
            code.emit(I.ASSIGN(var.localID, dtype, isConst))
            code.emit(I.PUSH(nil()))
        
        case array_append(lineNumber, element, array_name):
            codegen_(element)
            codegen_(array_name)
            code.emit(I.APPEND())
            code.emit(I.PUSH(nil()))
        
        case AtIndex(lineNumber, var, index):
            codegen_(index)
            codegen_(var)
            code.emit(I.ATINDEX())
        
        case SetAtIndex(lineNumber, var, index, value):
            codegen_(value)
            codegen_(index)
            codegen_(var)
            code.emit(I.SETATINDEX())
            code.emit(I.PUSH(nil()))
        
        case array_remove(lineNumber, index , var):
            codegen_(index)
            codegen_(var)
            code.emit(I.ARR_REMOVE())
        
        case array_insert(lineNumber, index, element, var):
            codegen_(element)
            codegen_(index)
            codegen_(var)
            code.emit(I.ARR_INSERT())
        
        case array_pop(lineNumber, var):
            codegen_(var)
            code.emit(I.ARR_POP())
        
        case array_len(lineNumber, var):
            codegen_(var)
            code.emit(I.ARRAY_LEN())
        
        case Slice(lineNumber, var, start, end):
            codegen_(end)
            codegen_(start)
            codegen_(var)
            code.emit(I.SLICE())
        
        case DeclareFun(lineNumber, f, return_type, params_type, params, body, function_type):
            EXIT = code.label()
            FBEGIN = code.label()
            code.emit(I.JMP(EXIT))
            code.emit_label(FBEGIN)
            for i in range(len(params)-1, -1, -1):
                code.emit(I.ASSIGN(params[i].localID, params_type[i], False))
            codegen_(body)
            code.emit(I.PUSH(nil()))
            code.emit(I.RETURN())
            code.emit_label(EXIT)
            code.emit(I.PUSHFN(FBEGIN))
            code.emit(I.ASSIGN(f.localID, CompiledFunction, False))
            code.emit(I.PUSH(nil()))
        
        case Return(lineNumber, value):
            codegen_(value)
            code.emit(I.RETURN())
        
        case FunCall(lineNumber, f, args):
            for arg in args:
                codegen_(arg)
            codegen_(f)
            code.emit(I.CALL())


        # Handling unknown expressions
        case _ as v:
            raise Exception(f"Got {v}, Expression|Statement Invalid")
