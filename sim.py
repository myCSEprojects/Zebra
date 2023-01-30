from dataclasses import dataclass
from fractions import Fraction
from typing import Union, Dict

@dataclass
class Variable:
    '''
    Variable class containing the name of the variable further
    evaluating to a data type in python
    '''
    name: str

# Basic Data Types
@dataclass
class Int:
   '''
   Class representing the integers in the language
   '''
   value: int

@dataclass
class Float:
    '''
    Floating objects represented as Fractions in python
    '''
    def __init__(self, value):
        self.value = Fraction(value)

@dataclass
class Bool:
    '''
    Seperate boolean class representing two types of values True and False
    '''
    value: bool

# Defined binary operators in the Language
BINARY_OPERATORS = [
                    "+", "/", "-", "//", "*", "%", "^", "-",    # Binary operators for numbers
                    "<<", ">>", "&", "|",                       # Bitwise binary operators for numbers
                    "<=", "<", ">", ">=", "==", "~=",           # Binary operators for Number types(similar)
                    "&&", "||", '='                             # Binary operators for Booleans
]

# Defined unary operators in the language
UNARY_OPERATORS = [
                    "-", # Unary operator for numbers
                    "~"  # Unary operator for Boolean types
]


# Basic Operations
@dataclass
class Let:
    '''
    Let class
    '''
    var: Variable
    e1: 'AST'
    e2: 'AST'

@dataclass
class If:
    '''
    If class evaluates to Bool
    '''
    condition: 'AST'
    ifBlock: 'AST'
    elseBlock: 'AST'

@dataclass
class BinOp:
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
    
    @staticmethod
    def raiseTypeError(operator, firstOperand, secondOperand):
        raise Exception(f"Operator {operator} not defined for operands of type {type(firstOperand)} and {type(secondOperand)}.")

    @staticmethod
    def checkSameType(operator, firstOperand, secondOperand):
        if (type(firstOperand) != type(secondOperand)):
            BinOp.raiseTypeError(operator, firstOperand, secondOperand)

    @staticmethod
    def checkType(operator, firstOperand, secondOperand, firstOperandType, secondOperandType):
        if (not(isinstance(firstOperand, firstOperandType)) or not(isinstance(secondOperand, secondOperandType))):
            BinOp.raiseTypeError(operator, firstOperand, secondOperand)

    



@dataclass
class UnOp:
    '''
    Variable evaluating to the value of the unary operation 
    '''
    operand: 'AST'
    operator: str

    @staticmethod
    def raiseTypeError(operator, operand):
        InvalidProgram(Exception(f"Operator {operator} not defined for the operand of type {type(operand)}."))

    @staticmethod
    def checkType(operator, operand, operandType):
        if (not isinstance(operand, operandType)):
            UnOp.raiseTypeError(operator, operand)
@dataclass
class none:
    noval: None


@dataclass
class Var:
    varia: Variable
    assignval: 'AST' = none

@dataclass
class PRINT:
    left: 'AST'
    right: 'AST'
    sep: str=' '



AST = Variable|BinOp|Bool|Int|Float|Let|If|UnOp|Var|none|PRINT
# Defining a Number as both an integer as  well as Float
Number = Float|Int

def InvalidProgram(exception ) -> None:
    raise exception

def evaluate(program: AST, environment: Dict[str,Variable] = {}):
    '''
    Evaluates the given AST
    '''
    match program:
        case Variable(name):
            if (name in environment):
                return evaluate(environment[name])
            else:
                InvalidProgram(Exception(f"Variable {name} not defined"))
        
        case Int(value):
            return program
        
        case Float(value):
            return program
        
        case Bool(value):
            return program

        case BinOp(operator, firstOperand, secondOperand):
            
            secondOperand = evaluate(secondOperand, environment)
            if(operator != "="):
                firstOperand = evaluate(firstOperand, environment)

            if (operator not in BINARY_OPERATORS):
                InvalidProgram(Exception(f"Operator {operator} not reconized"))
            
            match operator:
                case "+":
                    BinOp.checkType(operator, firstOperand, secondOperand, Number, Number)
                    
                    firstOperand, secondOperand = BinOp.implicitIntToFloat(firstOperand, secondOperand)
                    
                    if (isinstance(firstOperand, Float)):
                        return Float(firstOperand.value + secondOperand.value)
                    else:
                        return Int(firstOperand.value + secondOperand.value)

                case "-":
                    BinOp.checkType(operator, firstOperand, secondOperand, Number, Number)
                    
                    firstOperand, secondOperand = BinOp.implicitIntToFloat(firstOperand, secondOperand)
                    
                    if (isinstance(firstOperand, Float)):
                        return Float(firstOperand.value - secondOperand.value)
                    else:
                        return Int(firstOperand.value - secondOperand.value)
                
                case "/":
                    BinOp.checkType(operator, firstOperand, secondOperand, Number, Number)
                    # Checking if the denominator is zero
                    if (secondOperand == Int(0) or secondOperand == Float(0)):
                        InvalidProgram(Exception("Cannot divide with zero."))
                    return Float(firstOperand.value / secondOperand.value)
                
                case "*":
                    BinOp.checkType(operator, firstOperand, secondOperand, Number, Number)
                    
                    firstOperand, secondOperand = BinOp.implicitIntToFloat(firstOperand, secondOperand)
                    
                    if (isinstance(firstOperand, Float)):
                        return Float(firstOperand.value * secondOperand.value)
                    else:
                        return Int(firstOperand.value * secondOperand.value)
                
                case "//" :
                    
                    BinOp.checkType(operator, firstOperand, secondOperand, Number, Number)
                    # Checking if the denominator is zero
                    if (secondOperand == Int(0) or secondOperand == Float(0)):
                        InvalidProgram(Exception("Cannot divide with zero."))
                    return Int(int(firstOperand.value / secondOperand.value))
                
                case "%":
                    BinOp.checkType(operator, firstOperand, secondOperand, Int, Int)
                    return Int(firstOperand.value % secondOperand.value)
                
                case "<<":
                    BinOp.checkType(operator, firstOperand, secondOperand, Int, Int)
                    if (secondOperand.value < 0):
                        InvalidProgram(Exception(f"Negative left operand not allowed for {operator}."))
                    return Int(firstOperand.value << secondOperand.value)
                
                case ">>":
                    BinOp.checkType(operator, firstOperand, secondOperand, Int, Int)
                    if (secondOperand.value < 0):
                        InvalidProgram(Exception(f"Negative left operand not allowed for {operator}."))
                    return Int(firstOperand.value >> secondOperand.value)
                
                case "&":
                    BinOp.checkType(operator, firstOperand, secondOperand, Int, Int)
                    return Int(firstOperand.value & secondOperand.value)
                
                case "|":
                    BinOp.checkType(operator, firstOperand, secondOperand, Int, Int)
                    return Int(firstOperand.value | secondOperand.value)
                
                case "<=":
                    BinOp.checkSameType(operator, firstOperand, secondOperand)
                    BinOp.checkType(operator, firstOperand, secondOperand, Number, Number)
                    return Bool(firstOperand.value <= secondOperand.value)
                
                case "<":
                    BinOp.checkSameType(operator, firstOperand, secondOperand)
                    BinOp.checkType(operator, firstOperand, secondOperand, Number, Number)
                    return Bool(firstOperand.value < secondOperand.value)
                
                case "==":
                    BinOp.checkSameType(operator, firstOperand, secondOperand)
                    BinOp.checkType(operator, firstOperand, secondOperand, Number, Number)
                    return Bool(firstOperand.value == secondOperand.value) 
                
                case ">":
                    BinOp.checkSameType(operator, firstOperand, secondOperand)
                    BinOp.checkType(operator, firstOperand, secondOperand, Number, Number)
                    return Bool(firstOperand.value > secondOperand.value)
                
                case ">=":
                    BinOp.checkSameType(operator, firstOperand, secondOperand)
                    BinOp.checkType(operator, firstOperand, secondOperand, Number, Number)
                    return Bool(firstOperand.value >= secondOperand.value)
                
                case "!=":
                    BinOp.checkSameType(operator, firstOperand, secondOperand)
                    BinOp.checkType(operator, firstOperand, secondOperand, Number, Number)
                    return Bool(firstOperand.value != secondOperand.value)
                
                case "&&":
                    BinOp.checkType(operator, firstOperand, secondOperand, Bool, Bool)
                    return Bool(firstOperand.value and secondOperand.value)
                
                case "||":
                    BinOp.checkType(operator, firstOperand, secondOperand, Bool, Bool)
                    return Bool(firstOperand.value or secondOperand.value)
                case "=":
                    BinOp.checkType(operator, firstOperand, secondOperand, Variable, AST)
                    return evaluate(Var(firstOperand, secondOperand),environment)


        case UnOp(operator, operand):
            operand = evaluate(operand, environment)
            match operator:
                case "-":
                    UnOp.checkType(operator, operand, Number)

                    # Returning Literal similar to the operand literal
                    if (isinstance(operand, Float)):
                        return Float(operand.value * -1)
                    elif (isinstance(operand, Int)):
                        return Int(operand.value * -1)
                case "~":
                    UnOp.checkType(operator, operand, Bool)
                    return Bool(not operand.value)
        
        case Let (var, e1, e2):
            if (not isinstance(var, Variable)):
                InvalidProgram(Exception("Let expression parameter not of type Variable")) # To be completed
            return evaluate(e2, environment | {var.name: evaluate(e1)})

        case If (condition, ifBlock, elseBlock):
            evaluated_condition = evaluate(condition)
            if (not isinstance(evaluated_condition, Bool)):
                InvalidProgram(Exception(f"The condition {condition} does not evaluate to a boolean type"))
            if (evaluated_condition.value):
                return evaluate(ifBlock)
            else:
                if (elseBlock != None):
                    return evaluate(elseBlock)
                else:
                    return Bool(False)
        case Var(varia, assignval):
            if(type(assignval)==BinOp or type(assignval)==UnOp or type(assignval)==Let or type(assignval)==If):
                environment[varia.name]= evaluate(assignval, environment)
            else:
                environment[varia.name]= assignval
            return environment[varia.name]
        case PRINT(left, right, end):
            a=evaluate(left,environment)
            if(a!=None):
                print(a.value, end=end)
            b=evaluate(right, environment)
            if(b!=None):
                print(b.value, end=end)
            return
        #Handling unknown expressions
        case _:
           InvalidProgram(Exception("Expression Invalid"))


