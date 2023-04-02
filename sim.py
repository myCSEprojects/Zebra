from dataclasses import dataclass
from fractions import Fraction
from typing import Union, Optional, List, Dict
from lexer import Keyword, Operator, Identifier
from error import RuntimeError, typeCheckError, resolveError
import pprint

def traverse_list(lst):
    '''
    Utility for printing lists
    '''
    print_lst = []
    for ele in lst.elements:
        if isinstance(ele, zList):
            list_ele = traverse_list(ele)
            print_lst.append(list_ele)
        else:
            print_lst.append(ele.value)
    return print_lst

@dataclass
class metadata:
    '''
    Class to store the meta data of the AST
    '''
    lineNumber: int
@dataclass(frozen=True)
class Variable():
    '''
    Variable class containing the name of the variable
    '''
    lineNumber: int
    name: str
    id: int

    def __repr__(self):
        return f"{self.name}::{self.id}"

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

@dataclass
class zList():
    dtype : type
    elements : list

@dataclass
class FnObject:
    params_types: List[type]
    params: List[Variable]
    body: 'AST'
    return_type: type


@dataclass
class Scopes:
    '''
    Scopes storing the stack of environments
    '''
    stack: List[Dict[Variable, "AST"]]
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
        
    def declareFun(self, f: Variable, fn_object):
        #declares the function in the current scope with the give name v
        assert(len(self.stack) != 0)
        self.stack[-1][f] = [fn_object, FnObject, False]
    
    def declareVariable(self, var: Variable, value: 'AST', dtype:type, isConst: bool):
        '''
        Only declares a variable in the current scope
        '''
        assert(len(self.stack) != 0)
        # Avoiding redeclaration in the same scope
        # Implicit type conversion from float to int and int to float
        if (issubclass(dtype, Int)):
            if (isinstance(value, Float)):
                value = Int(int(value.value))
        
        elif (issubclass(dtype, Float)):
            if (isinstance(value, Int)):
                value = Float(float(value.value) if value.value != None else 0.0)
        elif (dtype != Bool and value != nil() and not isinstance(value, dtype)):
            typeCheckError(f"Cannot initialize a {dtype.__name__} with Literal of type {type(value).__name__}.", var.lineNumber)
        elif (dtype == Bool):
            value = Bool.truthy(value)
        self.stack[-1][var] = [value, dtype, isConst]
    
    def updateVariable(self, var: Variable, value: 'AST'):
        '''
        Utility to update the variable in the closest scope
        '''
        id = var.id
        name = var.name
        lineNumber = var.lineNumber

        for i in range(len(self.stack)-1, -1, -1):
            for var in self.stack[i]:
                if var.id == id:
                    # Truthify if lvalue is of type Bool
                    if (issubclass(self.stack[i][var][1], Bool)):
                        value = Bool.truthy(value)

                    if (self.getVariableIsConst(var) == True):
                        typeCheckError(f"Cannot Update const Variable {var.name}", lineNumber, "integrityError")
                    dtype = self.getVariableType(var)

                    # Implicit type conversion from float to int and int to float
                    if (issubclass(dtype, Int)):
                        if (isinstance(value, Float)):
                            value = Int(int(value.value))
                    
                    elif (issubclass(dtype, Float)):
                        if (isinstance(value, Int)):
                            value = Float(float(value.value) if value.value != None else 0.0)

                    elif (value != nil() and not isinstance(value, dtype)):
                        typeCheckError(f"Cannot assign {type(value).__name__} to a variable of type {dtype.__name__}", lineNumber)
                    
                    self.stack[i][var][0] = value
                    return value


    def getVariable(self, var: Variable):
        '''
        Utility to get the value of the variable in the closest scope
        '''
        for i in range(len(self.stack)-1, -1, -1):
            for v in self.stack[i]:
                if v.id == var.id:
                    return self.stack[i][v][0]
    
    def getVariableType(self, var: Variable):
        '''
          Utility to get the type of the variable in the closest scope
        '''
        for i in range(len(self.stack)-1, -1, -1):
            for v in self.stack[i]:
                if v.id == var.id:
                    return self.stack[i][v][1]
    
    def getVariableIsConst(self, var: Variable):
        '''
        Utility to get the constness of the variable in the closest scope
        '''
        for i in range(len(self.stack)-1, -1, -1):
            for v in self.stack[i]:
                if v.id == var.id:
                    return self.stack[i][v][2]

@dataclass
class list_pop(metadata):
    list_name : 'AST'

@dataclass
class Slice(metadata):
    value : 'AST' 
    first : Int 
    second : Int 

@dataclass
class list_append(metadata):
    element : 'AST'
    list_name : Identifier

@dataclass
class list_remove(metadata):
    index : Int
    list_name : Identifier

@dataclass 
class list_len(metadata):
    list_name : 'AST'

@dataclass 
class list_insert(metadata):
    index : Int
    element : 'AST'
    list_name : Identifier

# Basic Operations
@dataclass
class Declare(metadata):
    '''
    Declaration class
    '''
    var: Variable
    value: 'AST'
    dtype: type
    isConst: bool

@dataclass
class If(metadata):
    '''
    If class evaluates to Bool
    '''
    condition: 'AST'
    ifBlock: 'AST'
    elseBlock: 'AST'

@dataclass
class While(metadata):
    '''
    while loop
    '''
    condition: 'AST'
    block: 'AST'

@dataclass
class Block():
    '''
    Block Statement Introducing new Scope
    '''
    blockStatements: 'AST'

@dataclass
class BinOp(metadata):
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
class UnOp(metadata):
    '''
    Variable evaluating to the value of the unary operation 
    '''
    operator: str
    operand: 'AST'

@dataclass
class PRINT(metadata):
    print_stmt: List['AST']
    sep: Optional[str]=Str(' ')
    end: Optional[str]=Str('\n')

@dataclass
class Seq:
    lines: List['AST']


@dataclass
class For(metadata):
    initial : 'AST'
    condition : 'AST'
    block: 'AST'
        
@dataclass
class DeclareFun(metadata):
    var: Variable
    return_type: type
    params_type : List[type]
    params: List[Variable]
    body: 'AST'

@dataclass
class FunCall(metadata):
    fn: 'AST'
    args: List['AST']

@dataclass
class Return(metadata):
    value: 'AST'
    
# Defining the AST
AST = Variable|BinOp|Bool|Int|Float|Declare|If|UnOp|Str|Slice|nil|PRINT|Seq|For|DeclareFun|FunCall|zList|list_append|list_insert|list_len|list_remove|list_pop|Return

# Defining a Number as both an integer as  well as Float
Number = Float|Int


def evaluate(program: AST, scopes: Scopes = None):
    '''
    Evaluates the given AST
    '''
    # Generating a new scope if not provided
    if (scopes == None):
        scopes = Scopes()
    
    match program:
        case Variable(lineNumber, name, _) as v:
            return scopes.getVariable(v)
        
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
        
        case zList(dtype, value):
            return program

        case Block(blockStatements):
            # Creating a new scope
            scopes.beginScope()

            returnVal = evaluate(blockStatements, scopes)
            
            # Ending the current scope
            scopes.endScope()

            return returnVal

        case BinOp(lineNumber, operator, firstOperand, secondOperand):
            
            secondOperand = evaluate(secondOperand, scopes)
            
            if(operator != "="):
                firstOperand = evaluate(firstOperand, scopes)
            
            match operator:
                case "+":
                    #code for string concatenation starts
                    if (isinstance(firstOperand, Str) and isinstance(secondOperand, Str)):
                        return Str(firstOperand.value + secondOperand.value)
                    
                    if (isinstance(firstOperand, zList) and isinstance(secondOperand, zList)):
                        return zList(firstOperand.dtype, firstOperand.elements + secondOperand.elements)
                    
                    #code for string concatenation ends
                    
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
                        RuntimeError("Cannot divide with zero.", lineNumber)
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
                        RuntimeError("Cannot divide with zero.", lineNumber)
                    return Int(int(firstOperand.value / secondOperand.value))
                
                case "%":
                    return Int(firstOperand.value % secondOperand.value)
                
                case "<<":
                    if (secondOperand.value < 0):
                        RuntimeError(f"Negative left operand not allowed for {operator}.", lineNumber)
                    return Int(firstOperand.value << secondOperand.value)
                
                case ">>":
                    if (secondOperand.value < 0):
                        RuntimeError(f"Negative left operand not allowed for {operator}.", lineNumber)
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
                    return Bool(Bool.truthy(firstOperand).value and Bool.truthy(secondOperand).value)
                
                case "||":
                    return Bool(Bool.truthy(firstOperand).value or Bool.truthy(secondOperand).value)
                case "=":
                    return scopes.updateVariable(firstOperand, secondOperand)
                case "^":
                    if isinstance(firstOperand, Int) and isinstance(secondOperand, Int):
                        return Int(firstOperand.value ** secondOperand.value)
                    return Float(firstOperand.value ** secondOperand.value)

        case UnOp(lineNumber, operator, operand):
            operand = evaluate(operand, scopes)
            match operator:
                case "-":
                    # Returning Literal similar to the operand literal
                    if (isinstance(operand, Float)):
                        return Float(operand.value * -1)
                    elif (isinstance(operand, Int)):
                        return Int(operand.value * -1)
                case "~":
                    evaluated_operand = Bool.truthy(operand.value)
                    return Bool(not evaluated_operand.value)
        
        case Declare(lineNumber, var, value, dtype, isConst):
            # Evaluating the expression before declaration
            if (dtype == zList):
                if (value != nil()):
                    for i in range(len(value.elements)):
                        value.elements[i]=evaluate(value.elements[i], scopes)
            else:
                value = evaluate(value, scopes)
            
            # Truthify if Bool dtype
            if (dtype == Bool):
                value = Bool.truthy(value)
            # Declaring
            scopes.declareVariable(var, value, dtype, isConst)

            return value

        case If (lineNumber, condition, ifBlock, elseBlock):
            evaluated_condition = Bool.truthy(evaluate(condition, scopes))
            if (evaluated_condition.value):
                return evaluate(ifBlock, scopes)
            else:
                if (elseBlock != None): 
                    return evaluate(elseBlock, scopes)
                else:
                    return nil()

        case Slice(lineNumber, value_, first, second):
            elem = evaluate(value_, scopes)
            if(not(isinstance(elem, zList))):
                if (first.value>second.value or first.value < 0 or second.value > len(elem.value)):
                    RuntimeError("Index out of bounds", lineNumber, "indexError")
                
                return Str(elem.value[first.value:second.value])
            else:
                if (first.value < 0 or first.value >= len(elem.elements)):
                    RuntimeError("Index out of bounds", None, "indexError")
                if(second==nil()):
                    return elem.elements[first.value:first.value+1][0]
                if (first.value>second.value or first.value < 0 or second.value > len(elem.elements)):
                    RuntimeError("Index out of bounds", lineNumber, "indexError")
                return zList(elem.dtype, elem.elements[first.value:second.value])
        
        case PRINT(lineNumber, print_stmt, sep,end):
            for i,stmt in  enumerate(print_stmt):
                out=evaluate(stmt,scopes)
                if(isinstance(out,zList)):
                    l=traverse_list(out)
                    if (i==len(print_stmt)-1):
                        print(l, end=end.value)
                    else:
                        print(l, end=sep.value)
                elif (isinstance(out,nil)):
                    continue
                else:
                    if (i==len(print_stmt)-1):
                        print(out.value, end=end.value)
                    else:
                        print(out.value, end=sep.value)
            
            return nil()

        case Seq(lines):
            ans = nil()
            for line in lines:
                pp = pprint.PrettyPrinter(indent=4)
                # pp.pprint(line)
                ans = evaluate(line, scopes)
                match ans:
                    case Return(l,r):
                        # print("checkpoint:0")
                        break
                    case _:
                        continue
            return ans

        case While(lineNumber, condition,block) :
            while(evaluate(condition,scopes).value):
                evaluate(block,scopes)
            
            return nil()

        
        case For(lineNumber, initial,condition,block) :
            # evaluating the initialization and declaration condition
            scopes.beginScope()
            # run the initial statement(should not effect outrer scope)
            evaluate(initial,scopes)
            retVal = evaluate(While(lineNumber, condition,block),scopes)
            scopes.endScope()
            return retVal
        
        case list_append(lineNumber, element, var):
            l = scopes.getVariable(var)
            element=evaluate(element, scopes)
            l.elements.append(element)
            return nil()
        
        case list_remove(lineNumber, index , var):
            l=scopes.getVariable(var)
            # Checking if the index is out of bounds
            index=evaluate(index, scopes)
            if (len(l.elements) <= index.value):
                RuntimeError(f"list index out of bounds", lineNumber, 'indexError')
            return l.elements.pop(index.value)
        
        case list_len(lineNumber, var):
            l = evaluate(var, scopes)
            if(isinstance(l,zList)):
                return Int(len(l.elements))
            elif(isinstance(l,Str)):
                return Int(len(l.value))
        
        case list_pop(lineNumber, list_name):
            l=scopes.getVariable(list_name)
            if (len(l.elements) == 0):
                RuntimeError(f"Cannot popout from an empty list", lineNumber, 'indexError')
            return l.elements.pop()
        
        case list_insert(lineNumber, index, element, var):
            l = scopes.getVariable(var)
            element=evaluate(element, scopes)
            l.elements.insert(index.value, element)
            return nil()

        case DeclareFun(lineNumber, f, return_type, params_type, params, body):
            scopes.declareFun(f, FnObject(params_type, params, body, return_type))
            return nil()

        case FunCall(lineNumber, f, args): 
            fn = scopes.getVariable(f)
            # print('fn',fn)
            argv = []

            for arg in args:
                argv.append(evaluate(arg, scopes))

            scopes.beginScope()

            for i in range(len(fn.params)):
                scopes.declareVariable(fn.params[i],argv[i],fn.params_types[i],False)
        
            returnVal = evaluate(fn.body, scopes)

            scopes.endScope()
            
            match returnVal:
                case Return(lineNumber, value):
                    return evaluate(value, scopes)
                case _:
                    return nil()
            
        
        case Return(lineNumber, value):
            r =  evaluate(value, scopes)
            return Return(lineNumber,r)
    
        # Handling unknown expressions
        case _ as v:
            raise Exception(f"Got {v}, Expression|Statement Invalid")

