from sim import *
from error import typeCheckError, TypeCheckException
from dataclasses import dataclass
from typing import List, Dict, Union

isTypeCheckError = False

"""
NOTE: In some places we used python exception to raise errors that are not caught at any level.
This is because the error occured due to the bad functioning of the parser(and we want to correct them).
Some errors are to be shifted to the resolver pass and are also not caught at any level.(in Type check scopes)
"""

@dataclass
class TypecheckerScopes:
    '''
    Scopes storing the stack of environments
    '''
    def __init__(self, stack: List[Dict[str, 'AST']] = None):
        if (stack == None):
            self.stack = [dict()]
        else:
            self.stack = stack
    
    def beginScope(self): 
        self.stack.append({})
    
    def endScope(self):
        assert(len(self.stack) != 0)
        self.stack.pop()
    
    def declareVariable(self, var: Identifier, rtype: 'AST', ltype:'AST', isConst: bool, list_dtype: None):
        '''
        Only declares a variable in the current scope
        '''
        assert(len(self.stack) != 0)

        # Avoiding redeclaration in the same scope
        if var.val in self.stack[-1]:
            typeCheckError(f"Redeclaring already declared variable {var.val}", var.lineNumber, 'declareError')
        if (rtype != ltype):
            typeCheckError(f"Cannot initialize {ltype} with Literal of dtype {rtype}.", var.lineNumber)

        self.stack[-1][var.val] = [ltype, isConst]

        # Adding another list_dtype field to the scopes
        if (issubclass(ltype, zList)):
            self.stack[-1][var.val].append(list_dtype)
    
    def declareFun(self, f, fn_object):
        #declares the function in the current scope with the give name v
        assert(len(self.stack) != 0)

        if f.val in self.stack[-1]:
            raise Exception(f"Redeclaring already declared function {f.val}")
        
        self.stack[-1][f.val] = [fn_object, FnObject, False]
    
    def updateVariable(self, name: str, rtype: 'AST'):
        '''
        Utility to update the variable with the given name
        '''
        for i in range(len(self.stack)-1, -1, -1):
            if name in self.stack[i]:
                if (self.stack[i][name][1] == True):
                    raise Exception(f"Cannot Update const Variable {name}")
                if (rtype != self.stack[i][name][0]):
                    raise Exception(f"Cannot assign {rtype} to {self.stack[i][name][0]}")
                return
        
        raise Exception(f"Could not find the variable {name}.")

    def getVariable(self, name: str):
        '''
        Utility to get the value of the variable with the given name
        '''
        for i in range(len(self.stack)-1, -1, -1):
            if name in self.stack[i]:
                return self.stack[i][name]
        
        raise Exception(f"Could not resolve the variable {name}.")

Number = Int | Float


def typecheckAST(program: AST, scopes: TypecheckerScopes):
    '''
    Typechecks the given AST
    '''
    global isTypeCheckError
    try:
        typecheck(program, scopes)
    except TypeCheckException as e:
        isTypeCheckError = True
    return isTypeCheckError

def typecheckList(lst: zList, lineNumber: int):
    for element in lst.elements:
        element_ret = typecheck(element)
        if not issubclass(element_ret, lst.dtype):
            typeCheckError(f"Cannot initialize a list of type {lst.dtype} with element of type {type(element)}.", lineNumber)
        if isinstance(element_ret, zList):
            typecheckList(element, lineNumber)

def typecheck(program: AST, scopes = None):
    if (scopes == None):
        scopes = Scopes()
    match program:
        case Float(): 
            return Float
        case Int(): 
            return Int
        case Bool(): 
            return Bool
        case Variable(name):
            return scopes.getVariableType(name)
        case Str():
            return Str
        case nil():
            return nil
        case zList(dtype, lst):
            return zList
        case BinOp(operator, left, right):
            firstOperand = typecheck(left, scopes)
            secondOperand = typecheck(right, scopes)
            
            if (operator.val not in BINARY_OPERATORS):
                typeCheckError(f"Binary Operator {operator} not reconized", operator.lineNumber)
            
            match operator.val:
                case "+" | "-":
                    BinOp.checkType(operator, firstOperand, secondOperand, Number, Number)
                    
                    if (isinstance(firstOperand, Float)):
                        return Float
                    else:
                        return Int

                case "/":
                    BinOp.checkType(operator, firstOperand, secondOperand, Number, Number)
                    return Float
                
                case "*":
                    # for strings starts
                    second_type = isinstance(secondOperand,int) or isinstance(secondOperand,Int)
                    first_type = isinstance(firstOperand,int) or isinstance(firstOperand,Int)
                    
                    if (isinstance(firstOperand,Str) and second_type):
                        return Str

                    if (first_type and isinstance(secondOperand,Str)):
                        return Str
                    #for string ends

                    BinOp.checkType(operator, firstOperand, secondOperand, Number, Number)
                    
                    if (isinstance(firstOperand, Float)):
                        return Float
                    else:
                        return Int
                
                case "//" :
                    BinOp.checkType(operator, firstOperand, secondOperand, Number, Number)
                    return Int
                
                case "%" | "<<" | ">>" | "&" | "|":
                    BinOp.checkType(operator, firstOperand, secondOperand, Int, Int)
                    return Int
                
                
                case "<=" | "<" | "==" | ">" | ">=" | "!=":
                    BinOp.checkSameType(operator, firstOperand, secondOperand)
                    return Bool
                
                case "&&" | "||": 
                    BinOp.checkType(operator, firstOperand, secondOperand, AST, AST)
                    return Bool
                
                case "=":
                    BinOp.checkType(operator, type(left), secondOperand, Variable, AST)
                    
                    BinOp.checkSameType(operator, firstOperand, secondOperand|nil)
                    
                    # Prevent assignment for lists (for now)
                    if (issubclass(secondOperand, zList)):
                        typeCheckError(f"Cannot assign a list to a variable.", operator.lineNumber)

                    scopes.updateVariable(left.name, secondOperand(None))
                    return secondOperand

        case UnOp(operator, operand):   
            ot = typecheck(operand, scopes)
            if (operator.val not in UNARY_OPERATORS):
                typeCheckError(f"Unary Operator {operator} not reconized", operator.lineNumber)
            match operator.val:
                case "-":
                    UnOp.checkType(operator, ot, Number)

                    if (isinstance(ot, Float)):
                        return Float
                    else:
                        return Int
                case "~":
                    UnOp.checkType(operator, ot, Bool)
                    return Bool

        case Declare(var, value, dtype, isConst):
            if (not isinstance(var, Identifier)):
                raise Exception("RHS of declaration must be of type \'Identifier\'")

            # Make sure all the elements of the list are of the type zList.dtype
            if (dtype == zList):
                typecheckList(value, var.lineNumber)
                scopes.declareVariable(var, value, dtype, isConst)
            else:
                # Evaluating the expression before declaration
                value = typecheck(value, scopes)
                # Declaring
                scopes.declareVariable(var, dtype, value(None), isConst)
            return dtype

        case Slice(value_, first, second):       #checking value_ is string 
            tc = typecheck(value_, scopes)
            if (not(issubclass(tc, Str | zList))):
                raise Exception("Arguments passed to Slice must be of 'Str' type")
            return Str

        case While(condition,block) :            #checking while condition data type
            tc = typecheck(condition, scopes)
            if (not(issubclass(tc, AST))):
                raise Exception("Arguments passed to While block must be of 'AST' type")
            return nil
        
        case If (condition, ifBlock, elseBlock): #checking if condition data type
            tc = typecheck(condition, scopes)
            if (not (issubclass(tc, AST))):
                raise Exception("Arguments passed to If block must be of 'AST' type")
            return nil

        case For(initial,condition,block):
            tc1 =typecheck(initial, scopes)
            if(not(issubclass(tc1,AST))):
                raise Exception("Arguments passes to For initial must be of 'AST' type")
            tc = typecheck(condition, scopes)
            if(not( issubclass(tc,AST))):
                raise Exception("Arguments passes to For condition must be of 'AST' type")
            return nil

        case Seq(lines):
            ret = nil()
            for line in lines:
                ret = typecheck(line, scopes)
            return ret
        
        case PRINT(exps):
            for exp in exps:
                exp = typecheck(exp, scopes)
                # Make sure that the user does not ask for printing a list
                if (issubclass(exp, zList)):
                    typeCheckError(f"Cannot print a list.", None, "notPrintable")
                if (not issubclass(exp, AST)):
                    raise Exception(f"Invalid expression {exp} in PRINT")
            return nil
        
        case list_append(element, list_name):
            var_type = scopes.getVariableType(list_name.val)
            lIsConst = scopes.getVariableIsConst(list_name.val)
            lType = scopes.getVariable(list_name.val).dtype
            element=typecheck(element)
            if not(issubclass(var_type, zList)):
                typeCheckError(f"Cannot append an element of type {(element)} to a {var_type}.", None)
            elif lIsConst:
                typeCheckError(f"Cannot append an element to a constant list.", None, "constError")
            elif not (issubclass(element, lType)):
                typeCheckError(f"Cannot append an element of type {(element)} to a list of type {lType}.", None)
        
        case list_remove(index, list_name):
            var_type = scopes.getVariableType(list_name.val)
            lIsConst = scopes.getVariableIsConst(list_name.val)
            if not(issubclass(var_type, zList)):
                typeCheckError(f"Cannot remove an element from {var_type}.", None)
            elif lIsConst:
                typeCheckError(f"Cannot remove an element from a constant list.", None, "constError")
            
        case list_len(list_name):
            varType = scopes.getVariableType(list_name.val)
            if not(issubclass(varType, zList)):
                typeCheckError(f"Cannot remove an element from {varType}.", None)
            return Int
        
        case list_insert(index, element, list_name):
            var_type = scopes.getVariableType(list_name.val)
            lIsConst = scopes.getVariableIsConst(list_name.val)
            lType = scopes.getVariable(list_name.val).dtype
            element=typecheck(element)
            index=typecheck(index)
            if not(issubclass(var_type, zList)):
                typeCheckError(f"Cannot append an element of type {element} to a {var_type}.", None)
            elif lIsConst:
                typeCheckError(f"Cannot append an element to a constant list.", None, "constError")
            elif not (issubclass(index, Int)):
                typeCheckError(f"index must be an integer.", None)
            elif not (issubclass(element, lType)):
                typeCheckError(f"Cannot append an element of type {element} to a list of type {lType}.", None)
                
        case DeclareFun(Identifier(lineNumber, _) as f, return_type, params_type, params, body):
            scopes.declareFun(f, FnObject(params_type, params, body, return_type)) 

        case FunCall(Identifier(lineNumber, _) as f, args): 
            fn = scopes.getVariable(f.val)
            argv = []

            for arg in args:
                argv.append(typecheck(arg, scopes))

            scopes.beginScope()
            
            for param, arg in zip(fn.params, argv):
                scopes.declareVariable(param,arg(None),arg,False)

            p_types = fn.params_types

            for len_ in range(len(p_types)):
                if (not(issubclass(p_types[len_],(argv[len_])))):
                    raise Exception(f" {len_+1}th Argument passed to the function is of invalid type")

            ret_type = fn.return_type 
            eval_type = typecheck(fn.body,scopes)

            if (not(issubclass(eval_type,ret_type))):
                raise Exception("Invalid type returned by the function")
        
            scopes.endScope()
            return ret_type

        case _:
            raise Exception("Type checking failed.")
