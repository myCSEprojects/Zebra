from typing import List
from sim import *
from instruction_list import Instruction
from instructions import I, Label
from codegen import CompiledFunction, ByteCode

class Frame:
    locals: List[AST]
    returnAddress: int
    dynamicLink: 'Frame'
    staticLink: 'Frame'

    def __init__(self, returnAddress: None, dynamicLink: None, staticLink: None):
        MAX_LOCALS = 32
        self.locals = [None] * MAX_LOCALS
        self.returnAddress = returnAddress
        self.dynamicLink = dynamicLink
        self.staticLink = staticLink


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
        self.currentFrame = Frame(None, None, None)

    def jump(self, jumps):
        temp_frame = self.currentFrame
        while jumps:
            temp_frame = temp_frame.staticLink
            jumps -= 1
        return temp_frame

    def execute(self) -> AST:
        while True:
            assert self.ip < len(self.bytecode.inst)
            # print(self.bytecode.inst[self.ip])
            match self.bytecode.inst[self.ip]:
                case I.PUSH(val):
                    self.data.append(val)
                    self.ip += 1

                case I.PUSHFN(Label(offset)):
                    self.data.append(CompiledFunction(offset, self.currentFrame))
                    self.ip += 1

                case I.CALL():
                    cf = self.data.pop()
                    self.currentFrame = Frame (returnAddress=self.ip + 1, dynamicLink=self.currentFrame, staticLink=cf.staticLink)
                    self.ip = cf.entry

                case I.RETURN():
                    self.ip = self.currentFrame.returnAddress
                    self.currentFrame = self.currentFrame.dynamicLink

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
                        self.ip += 1
                    elif (isinstance(firstOperand, zArray)):
                        self.data.append(zArray(-1, firstOperand.dtype, firstOperand.elements + secondOperand.elements))
                        self.ip += 1
                    firstOperand, secondOperand = BinOp.implicitIntToFloat(firstOperand, secondOperand)
                    if (isinstance(firstOperand, Float)):
                        self.data.append(Float(firstOperand.value + secondOperand.value))
                        self.ip += 1
                    elif (isinstance(firstOperand, Int)):
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
                
                case I.JMP(label):
                    self.ip = label.target
                
                case I.JMP_IF_FALSE(label):
                    op = self.data.pop()
                    if not op.value:
                        self.ip = label.target 
                    else:
                        self.ip += 1
                
                case I.JMP_IF_TRUE(label):
                    op = self.data.pop()
                    if op.value:
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
                
                case I.PRINT(end):
                    p=self.data.pop()
                    if(isinstance(p,zArray)):
                        l=traverse_array(p)
                        print(l, end=end)
                    elif (isinstance(p,nil)):
                        print(end)
                    else:
                        print(p, end=end)
                    self.ip+=1
                
                case I.LOAD(localID, staticJumps):
                    frame =  self.jump(staticJumps)
                    self.data.append(frame.locals[localID][0])
                    self.ip += 1
                
                case I.COLL_ARR(size, arrayType, lineNumber):
                    l = []
                    for _ in range(size):
                        l.append(self.data.pop())
                    self.data.append(zArray(lineNumber, arrayType, l))
                    self.ip += 1
                
                case I.STORE(localID, staticJumps):
                    frame = self.jump(staticJumps)
                    v = self.data.pop()
                    if isinstance(v, Float) and dtype == Int:
                        v = Int(int(v.value))
                    elif isinstance(v, Int) and dtype == Float:
                        v = Float(float(v.value))
                    frame.locals[localID][0] = v
                    self.ip += 1
                
                case I.ASSIGN(localID, dtype, isConst):
                    v=self.data.pop()
                    if isinstance(v, Float) and dtype == Int:
                        v = Int(int(v.value))
                    elif isinstance(v, Int) and dtype == Float:
                        v = Float(float(v.value))
                    self.currentFrame.locals[localID]=[v,dtype,isConst]
                    self.ip+=1
                
                case I.APPEND():
                    secondOperand = self.data.pop()
                    firstOperand = self.data.pop()
                    secondOperand.elements.append(firstOperand)
                    self.ip += 1
                
                case I.ATINDEX():
                    value = self.data.pop()
                    index = self.data.pop()
                    if isinstance(value, zArray):
                        if index.value >= len(value.elements) or index.value < 0:
                            RuntimeError("Index out of bounds.", -1)
                        self.data.append(value.elements[index.value])
                    else:
                        if index.value >= len(value.value) or index.value < 0:
                            RuntimeError("Index out of bounds.", -1)
                        self.data.append(Str(value.value[index.value]))
                    self.ip += 1

                case I.SETATINDEX():
                    var = self.data.pop()
                    index = self.data.pop()
                    value = self.data.pop()
                    if isinstance(var, zArray):
                        if index.value >= len(var.elements) or index.value < 0:
                            RuntimeError("Index out of bounds.", -1)
                        var.elements[index.value] = value
                    else:
                        if index.value >= len(var.value) or index.value < 0:
                            RuntimeError("Index out of bounds.", -1)
                        var.value = var.value[:index.value] + value.value + var.value[index.value+1:]
                    self.ip += 1
                
                case I.ARRAY_LEN():
                    value = self.data.pop()
                    if isinstance(value, zArray):
                        self.data.append(Int(len(value.elements)))
                    else:
                        self.data.append(Int(len(value.value)))
                    self.ip += 1
                
                case I.SLICE():
                    value = self.data.pop()
                    start = self.data.pop()
                    end = self.data.pop()
                    
                    if start.value > end.value:
                        RuntimeError("Start index cannot be greater than end index.", -1)
                    
                    if isinstance(value, zArray):
                        if start.value < 0 or end.value < 0:
                            RuntimeError("Negative slice operand not allowed.", -1)
                        elif start.value > len(value.elements) or end.value > len(value.elements):
                            RuntimeError("Index out of bounds", -1)
                        self.data.append(zArray(-1, value.dtype, value.elements[start.value:end.value]))
                    else:
                        if start.value < 0 or end.value < 0:
                            RuntimeError("Negative slice operand not allowed.", -1)
                        elif start.value > len(value.value) or end.value > len(value.value):
                            RuntimeError("Index out of bounds", -1)
                        self.data.append(Str(value.value[start.value:end.value]))
                    self.ip += 1
                
                case I.ARR_REMOVE():
                    value = self.data.pop()
                    index = self.data.pop()

                    if index.value > len(value.elements) or index.value < 0:
                        RuntimeError("Index out of bounds", -1)

                    value.elements.pop(index.value)
                    self.data.append(nil())
                    self.ip += 1
                
                case I.ARR_INSERT():
                    value = self.data.pop()
                    index = self.data.pop()
                    element = self.data.pop()
                    if index.value > len(value.elements) or index.value < 0:
                        RuntimeError("Index out of bounds", -1)
                    value.elements.insert(index.value, element)
                    self.data.append(nil())
                    self.ip += 1
                
                case I.ARR_POP():
                    value = self.data.pop()
                    if len(value.elements) == 0:
                        RuntimeError("Cannot pop from empty array", -1)
                    value.elements.pop()
                    self.data.append(nil())
                    self.ip += 1

                case I.HALT():
                    return self.data.pop()