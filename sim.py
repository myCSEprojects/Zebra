from dataclasses import dataclass
from fractions import Fraction
from typing import Union, Dict, List

@dataclass
class Variable:
    '''
    Variable class containing the name of the variable further
    evaluating to a data type in python
    '''
    name: str
@dataclass
class nil:
    noval = None
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
    @staticmethod
    def truthy(checking):
        if(checking == Int(0) or checking == Str("") or checking == Float(0) or checking == nil() or checking == Bool(False)):
            return Bool(False)
        else:
            return Bool(True)

@dataclass
class Str :
    value: str

@dataclass
class Slice:
    value : 'AST' 
    first : Int 
    second : Int 


# Defined binary operators in the Language
BINARY_OPERATORS = [
                    "+", "/", "-", "//", "*", "%", "^", "-",     # Binary operators for numbers
                    "<<", ">>", "&", "|",                       # Bitwise binary operators for numbers
                    "<=", "<", ">", ">=", "==", "~=",           # Binary operators for Number types(similar)
                    "&&", "||"  , "="                                # Binary operators for Booleans
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
class str_concat:
    #function to concat the strings passed as an argument list
    Left : 'AST'
    Right : 'AST'


@dataclass
class Loop:
    '''
    loop(variable,steps,block)
    '''
    var: Variable
    steps: 'AST'
    block: 'AST'


@dataclass
class While:
    '''
    while loop
    '''
    condition: 'AST'
    block: 'AST'
    
    

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
class PRINT:
    left: 'AST'
    right: 'AST'
    sep: str=' '
@dataclass
class Seq:
    lines: List['AST']

@dataclass
class truthy:
    arg : 'AST'

AST = Variable|BinOp|Bool|Int|Float|Let|If|UnOp|Str|str_concat|Slice|nil|PRINT|Seq|truthy
# Defining a Number as both an integer as  well as Float
Number = Float|Int

def InvalidProgram(exception ) -> None:
    raise exception

def evaluate(program: AST, environment: Dict[str,Variable] = None):
    '''
    Evaluates the given AST
    '''
    if (environment == None):
        environment = {}

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

        case Str(value):
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
                    # for strings starts
                    second_type = isinstance(secondOperand,int) or isinstance(secondOperand,Int)
                    first_type = isinstance(firstOperand,int) or isinstance(firstOperand,Int)
                    
                    if (isinstance(firstOperand,Str) and second_type):
                        return Str(firstOperand.value * secondOperand.value)

                    if (first_type and isinstance(secondOperand,Str)):
                        return Str(firstOperand.value * secondOperand.value)
                    #for string ends

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
                    secondOperand = evaluate(secondOperand, environment)
                    environment[firstOperand.name]= secondOperand
                    return secondOperand

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
                InvalidProgram(Exception("Let expression parameter not of type Variable")) 
            return evaluate(e2, environment | {var.name: evaluate(e1)})

        case If (condition, ifBlock, elseBlock):
            evaluated_condition = Bool.truthy(evaluate(condition))
            if (not isinstance(evaluated_condition, Bool)):
                InvalidProgram(Exception(f"The condition {condition} does not evaluate to a boolean type"))
            if (evaluated_condition.value):
                return evaluate(ifBlock)
            else:
                if (elseBlock != None): 
                    return evaluate(elseBlock)
                else:
                    return Bool(False)

        case str_concat(left,right):
            
            elem1 = evaluate(left)
            elem2 = evaluate(right)
            if (not(isinstance(elem1,Str) and isinstance(elem2,Str))):
                InvalidProgram(Exception("Arguments passed to str_concat() must be of 'Str' type"))
            return Str(elem1.value+elem2.value)


        case Slice(value_, first, second):
            elem = evaluate(value_)

            if (not (isinstance(elem,Str))):
                InvalidProgram(Exception("Arguments passed to Slice() must be of 'Str' type"))
            
            if (first>second or first < 0 or second > len(elem.value)):
                InvalidProgram(Exception("Invalid index"))
            return Str(elem.value[first:second])
        
        case PRINT(left, right, end):
            a=evaluate(left,environment)
            if(a!=None):
                print(a.value, end=end)
            b=evaluate(right, environment)
            if(b!=None):
                print(b.value, end=end)
            return

        case Seq(lines):
            ans = None
            for line in lines:
                ans = evaluate(line, environment)
            return ans
        
        case Loop(Variable(var),steps,block) :
            steps = evaluate(steps,environment)
            environment = environment | {var:steps}
            if (steps == Int(0)) :
                return Bool(False)
            else :
                environment[var] = steps
                evaluate(block,environment)
                return evaluate(Loop(Variable(var),BinOp("-",steps,Int(1)), block),environment)

        case While(condition,block) :
            evaluated_condition = evaluate(condition,environment)
            if (not isinstance(evaluated_condition, Bool)):
                InvalidProgram(Exception(f"The condition {condition} does not evaluate to a boolean type"))
            if (evaluated_condition.value):
                evaluate(block,environment)
                return evaluate(While(condition,block),environment)
            else :
                return Bool(False)

    
        # Handling unknown expressions
        case _:
            InvalidProgram(Exception("Expression Invalid"))

