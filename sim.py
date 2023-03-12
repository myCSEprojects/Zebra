from dataclasses import dataclass
from fractions import Fraction
from typing import Union, Optional, List, Dict
from lexer import Keyword, Operator, Identifier
from error import RuntimeError, typeCheckError

@dataclass
class Variable:
    '''
    Variable class containing the name of the variable
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
    value: Fraction
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
class nil:
    noval = None

@dataclass
class Slice:
    value : 'AST' 
    first : Int 
    second : Int 


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


# Basic Operations
@dataclass
class Declare:
    '''
    Declaration class
    '''
    var: Identifier
    value: 'AST'
    dtype: type
    isConst: bool

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
class Scopes:
    '''
    Scopes storing the stack of environments
    '''
    def __init__(self, stack: List[Dict[Variable, "AST"]] = None):
        if (stack == None):
            self.stack = [dict()]
        else:
            self.stack = stack
    
    def beginScope(self):
        self.stack.append({})
    
    def endScope(self):
        assert(len(self.stack) != 0)
        self.stack.pop()
        
    def declareFun(self, v, fn_object):
        #declares the function in the current scope with the give name v
        assert(len(self.stack) != 0)
        self.stack[-1][v.name] = [fn_object, FnObject, False]
    
    def declareVariable(self, var: Identifier, value: 'AST', dtype:type, isConst: bool):
        '''
        Only declares a variable in the current scope
        '''
        assert(len(self.stack) != 0)
        self.stack[-1][var.val] = [value, dtype, isConst]
    
    def updateVariable(self, name: str, value: 'AST'):
        '''
        Utility to update the variable in the closest scope
        '''
        for i in range(len(self.stack)-1, -1, -1):
            if name in self.stack[i]:
                
                # Truthify if lvalue is of type Bool
                if (issubclass(self.stack[i][name][1], Bool)):
                    value = Bool.truthy(value)
                
                self.stack[i][name][0] = value
                return value

    def getVariable(self, name: str):
        for i in range(len(self.stack)-1, -1, -1):
            if name in self.stack[i]:
                return self.stack[i][name][0]

@dataclass
class Block:
    '''
    Block Statement Introducing new Scope
    '''
    blockStatements: 'AST'

@dataclass
class BinOp:
    '''
    Variable evaluting to the value of the binary operation
    '''
    operator: Operator
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
        typeCheckError(f"Operator {operator.val} not defined for operands of type {(firstOperand)} and {(secondOperand)}.", operator.lineNumber)

    @staticmethod
    def checkSameType(operator, firstOperand, secondOperand):
        if (not issubclass((firstOperand),(secondOperand))):
            BinOp.raiseTypeError(operator, firstOperand, secondOperand)

    @staticmethod
    def checkType(operator, firstOperand, secondOperand, firstOperandType, secondOperandType):
        if (not(issubclass(firstOperand, firstOperandType)) or not(issubclass(secondOperand, secondOperandType))):
            BinOp.raiseTypeError(operator, firstOperand, secondOperand)


@dataclass
class UnOp:
    '''
    Variable evaluating to the value of the unary operation 
    '''
    operand: 'AST'
    operator: Operator

    @staticmethod
    def raiseTypeError(operator, operand):
        typeCheckError(f"Operator {operator.val} not defined for the operand of type {(operand)}.", operator.lineNumber)

    @staticmethod
    def checkType(operator, operand, operandType):
        if (not issubclass(operand,operandType)):
            UnOp.raiseTypeError(operator, operand)
@dataclass
class PRINT:
    print_stmt: List['AST']
    sep: Optional[str]=' '

@dataclass
class Seq:
    lines: List['AST']


@dataclass
class For:
    initial : 'AST'
    condition : 'AST'
    block: 'AST'
        
@dataclass
class DeclareFun:
    name: 'AST'
    params: List['AST']
    body: 'AST'

@dataclass
class FunCall:
    fn: 'AST'
    args: List['AST']

@dataclass
class FnObject:
    params: List['AST']
    body: 'AST'
    
# Defining the AST
AST = Variable|BinOp|Bool|Int|Float|Declare|If|UnOp|Str|str_concat|Slice|nil|PRINT|Seq|For

# Defining a Number as both an integer as  well as Float
Number = Float|Int

def evaluate(program: AST, scopes: Scopes = None):
    '''
    Evaluates the given AST
    '''
    if (scopes == None):
        scopes = Scopes()
    match program:
        case Variable(name):
            return scopes.getVariable(name)
        
        case Int(value):
            return program
        
        case Float(value):
            return program
        
        case Bool(value):
            return program

        case Str(value):
            return program

        case nil():
            return program

        case Block(blockStatements):
            # Creating a new scope
            scopes.beginScope()

            returnVal = evaluate(blockStatements, scopes)
            
            # Ending the current scope
            scopes.endScope()

            return returnVal

        case BinOp(operator, firstOperand, secondOperand):
            
            secondOperand = evaluate(secondOperand, scopes)
            
            if(operator.val != "="):
                firstOperand = evaluate(firstOperand, scopes)
            
            match operator.val:
                case "+":
                    firstOperand, secondOperand = BinOp.implicitIntToFloat(firstOperand, secondOperand)
                    
                    if (isinstance(firstOperand, Float)):
                        return Float(firstOperand.value + secondOperand.value)
                    else:
                        return Int(firstOperand.value + secondOperand.value)

                case "-":
                    firstOperand, secondOperand = BinOp.implicitIntToFloat(firstOperand, secondOperand)
                    
                    if (isinstance(firstOperand, Float)):
                        return Float(firstOperand.value - secondOperand.value)
                    else:
                        return Int(firstOperand.value - secondOperand.value)
                
                case "/":
                    if (secondOperand == Int(0) or secondOperand == Float(0)):
                        RuntimeError("Cannot divide with zero.", operator.lineNumber)
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
                    
                    firstOperand, secondOperand = BinOp.implicitIntToFloat(firstOperand, secondOperand)
                    
                    if (isinstance(firstOperand, Float)):
                        return Float(firstOperand.value * secondOperand.value)
                    else:
                        return Int(firstOperand.value * secondOperand.value)
                
                case "//" :
                    if (secondOperand == Int(0) or secondOperand == Float(0)):
                        RuntimeError("Cannot divide with zero.", operator.lineNumber)
                    return Int(int(firstOperand.value / secondOperand.value))
                
                case "%":
                    return Int(firstOperand.value % secondOperand.value)
                
                case "<<":
                    if (secondOperand.value < 0):
                        RuntimeError(f"Negative left operand not allowed for {operator}.", operator.lineNumber)
                    return Int(firstOperand.value << secondOperand.value)
                
                case ">>":
                    if (secondOperand.value < 0):
                        RuntimeError(f"Negative left operand not allowed for {operator}.", operator.lineNumber)
                    return Int(firstOperand.value >> secondOperand.value)
                
                case "&":
                    return Int(firstOperand.value & secondOperand.value)
                
                case "|":
                    return Int(firstOperand.value | secondOperand.value)
                
                case "<=":
                    return Bool(firstOperand.value <= secondOperand.value)
                
                case "<":
                    return Bool(firstOperand.value < secondOperand.value)
                
                case "==":
                    return Bool(firstOperand.value == secondOperand.value) 
                
                case ">":
                    return Bool(firstOperand.value > secondOperand.value)
                
                case ">=":
                    return Bool(firstOperand.value >= secondOperand.value)
                
                case "!=":
                    return Bool(firstOperand.value != secondOperand.value)
                
                case "&&":
                    return Bool(firstOperand.value and secondOperand.value)
                
                case "||":
                    return Bool(firstOperand.value or secondOperand.value)
                case "=":
                    return scopes.updateVariable(firstOperand.name, secondOperand)

        case UnOp(operator, operand):
            operand = evaluate(operand, scopes)
            match operator.val:
                case "-":
                    # Returning Literal similar to the operand literal
                    if (isinstance(operand, Float)):
                        return Float(operand.value * -1)
                    elif (isinstance(operand, Int)):
                        return Int(operand.value * -1)
                case "~":
                    evaluated_operand = Bool.truthy(operand.value)
                    return Bool(not evaluated_operand.value)
        
        case Declare(var, value, dtype, isConst):
            
            # Evaluating the expression before declaration
            value = evaluate(value, scopes)

            # Truthify if Bool dtype
            if (dtype == Bool):
                value = Bool.truthy(value)

            # Declaring
            scopes.declareVariable(var, value, dtype, isConst)

            return value

        case If (condition, ifBlock, elseBlock):
            evaluated_condition = Bool.truthy(evaluate(condition, scopes))
            
            if (evaluated_condition.value):
                return evaluate(ifBlock, scopes)
            else:
                if (elseBlock != None): 
                    return evaluate(elseBlock, scopes)
                else:
                    return Bool(False)

        # case str_concat(left,right):
            
        #     elem1 = evaluate(left, scopes)
        #     elem2 = evaluate(right, scopes)
        #     if (not(isinstance(elem1,Str) and isinstance(elem2,Str))):
        #         InvalidProgram(Exception("Arguments passed to str_concat() must be of 'Str' type"))
        #     return Str(elem1.value+elem2.value)


        case Slice(value_, first, second):
            elem = evaluate(value_, scopes)

            if (first>second or first < 0 or second > len(elem.value)):
                raise Exception("Index out of bounds")
            
            return Str(elem.value[first:second])
        
        case PRINT(print_stmt, end):
            ans=None
            for stmt in print_stmt:
                ans=evaluate(stmt,scopes)
                print(ans.value, end=end)
            print()
            return nil()

        case Seq(lines):
            ans = nil()
            for line in lines:
                ans = evaluate(line, scopes)
            return ans
        
        case Loop(var,steps,block) :
            steps = evaluate(steps,scopes)
            scopes.updateVariable(var.name, steps)
            if (steps == Int(0)) :
                return Bool(False)
            else :
                evaluate(block,scopes)
                return evaluate(Loop(var,BinOp("-",steps,Int(1)), block),scopes)

        case While(condition,block) :
            evaluated_condition = evaluate(condition,scopes)
            if (evaluated_condition.value):
                evaluate(block,scopes)
                return evaluate(While(condition,block),scopes)
            else :
                return Bool(False)
        
        case For(initial,condition,block) :
            # evaluating the initialization and declaration condition
            if (initial != nil()) :
                evaluate(initial,scopes)
            return evaluate(While(condition,block),scopes)
        
        case DeclareFun(Variable(_) as v, params, body):
            scopes.declareFun(v, FnObject(params, body))
        

        case FunCall(Variable(_) as v, args):
            
            fn = scopes.getVariable(v.name)
            #print(fn)
            argv = []
            for arg in args:
                argv.append(evaluate(arg,scopes))

            scopes.beginScope()

            for param, arg in zip(fn.params, argv):
                scopes.declareVariable(param,arg,'AST',False)
        

            v = evaluate(fn.body, scopes)
            scopes.endScope()

            return v
    
        # Handling unknown expressions
        case _:
            raise Exception("Expression|Statement Invalid")

