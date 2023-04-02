from sim import *
from error import typeCheckError, TypeCheckException
from dataclasses import dataclass
from typing import List, Dict, Union

"""
NOTE: In some places we used python exception to raise errors that are not caught at any level.
This is because the error occured due to the bad functioning of the parser(and we want to correct them).
Some errors are to be shifted to the resolver pass and are also not caught at any level.(in Type check scopes)
"""

# Some Utility functions
def checkTypeTwo(firstOperandType: AST, secondOperandType: AST, firstType: type, secondType: type):
    '''
    Utility to check the type of the operands
    '''
    if not issubclass(firstOperandType, firstType):
        return False
    if not issubclass(secondOperandType, secondType):
        return False
    return True

def checkSameType(firstOperandType: AST, secondOperandType: AST):
    '''
    Utility to check the if both operands are of the same type
    '''
    if not (issubclass(firstOperandType, secondOperandType) and issubclass(firstOperandType, secondOperandType)):
        return False
    return True

Number = Int | Float

def createDummyObject(type_ : type):
    '''
    Utility to Create a dummy(useles) object from the given type
    '''
    if type_ == Int or type_ == Bool or type_ == Str:
        return type_(None)
    elif type_ == Float:
        return Float(0)
    elif type_ == nil:
        return nil()
    elif issubclass(type_, zList):
        return zList(None, None)


def typecheckAST(program: AST, scopes: Scopes):
    '''
    Typechecks the given AST
    '''
    try:
        typecheck(program, scopes)
    except TypeCheckException as e:
        raise e

def typecheckList(lst: zList, lineNumber: int, scopes:Scopes):
    for element in lst.elements:
        element_ret = typecheck(element, scopes)
        if not issubclass(element_ret, lst.dtype):
            typeCheckError(f"Cannot initialize a list of type {lst.dtype} with element of type {type(element)}.", lineNumber)
        if isinstance(element_ret, zList):
            typecheckList(element, lineNumber, scopes)
    return zList

def dimensions(lst):
    if isinstance(lst, zList):
        return [len(lst.elements)] + dimensions(lst.elements[0])
    else:
        return []

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
        case Variable(lineNumber, name, id) as v:
            return scopes.getVariableType(v)
        case Str():
            return Str
        case nil():
            return nil
        case zList(dtype, lst):
            return zList
        case BinOp(lineNumber, operator, firstOperand, secondOperand):
            # Getting the operand types
            firstOperandType = typecheck(firstOperand, scopes)
            secondOperandType = typecheck(secondOperand, scopes)
            
            # Checking if the operator is defined
            if (operator not in BINARY_OPERATORS):
                typeCheckError(f"Binary Operator {operator} not reconized", lineNumber)

            # General BinOp type error string
            errorString = f"Operator {operator} not defined between data types {firstOperandType.__name__} and {secondOperandType.__name__}"

            match operator:
                case  "+":
                    if (issubclass(firstOperandType, Str) and not checkTypeTwo(firstOperandType, secondOperandType, Str, Str)):
                        typeCheckError(errorString, lineNumber)
                    elif (issubclass(firstOperandType, zList) and not checkTypeTwo(firstOperandType, secondOperandType, zList, zList)):
                        typeCheckError(errorString, lineNumber)
                    elif (issubclass(firstOperandType, Number) and not checkTypeTwo(firstOperandType, secondOperandType, Number, Number)):
                        typeCheckError(errorString, lineNumber)

                    if (issubclass(firstOperandType, Float) or issubclass(secondOperandType, Float)):
                        return Float
                    elif (issubclass(firstOperandType, Str)):
                        return Str
                    elif (issubclass(firstOperandType, zList)):
                        fo=scopes.getVariable(firstOperand)
                        so=scopes.getVariable(secondOperand)
                        l1=dimensions(fo)
                        l2=dimensions(so)
                        if(l1!=l2):
                            typeCheckError(f"Cannot append arrays of two different dimensions", lineNumber)
                        return zList
                    else:
                        return Int
                    
                case  "-":
                    if not checkTypeTwo(firstOperandType, secondOperandType, Number, Number):
                        typeCheckError(errorString, lineNumber)
                    
                    if (issubclass(firstOperandType, Float) or issubclass(secondOperandType, Float)):
                        return Float
                    else:
                        return Int

                case "/":
                    if not checkTypeTwo(firstOperandType, secondOperandType, Number, Number):
                        typeCheckError(errorString, lineNumber)
                    return Float
                
                case "*":
                    if (issubclass(firstOperandType,Str) and issubclass(secondOperandType, Int)):
                        return Str

                    elif (issubclass(firstOperandType,Int) and issubclass(secondOperandType,Str)):
                        return Str
                    elif not checkTypeTwo(firstOperandType, secondOperandType, Number, Number):
                        typeCheckError(errorString, lineNumber)
                    else:
                        if (issubclass(firstOperandType, Float) | issubclass(secondOperandType, Float)):
                            return Float
                        else:
                            return Int
                
                case "//" :
                    if not checkTypeTwo(firstOperandType, secondOperandType, Number, Number):
                        typeCheckError(errorString, lineNumber)
                    return Int
                
                case "%" | "<<" | ">>" | "&" | "|":
                    if not checkTypeTwo(firstOperandType, secondOperandType, Int, Int):
                        typeCheckError(errorString, lineNumber)
                    return Int
                
                
                case "<=" | "<" | "==" | ">" | ">=" | "!=":
                    if not checkSameType(firstOperandType, secondOperandType):
                        typeCheckError(errorString, lineNumber)
                    return Bool
                
                case "&&" | "||": 
                    if not checkTypeTwo(firstOperandType, secondOperandType, AST, AST):
                        typeCheckError(errorString, lineNumber)
                    return Bool
                
                case "=":                    
                    # Prevent assignment for lists (for now)
                    if (issubclass(secondOperandType, zList)):
                        typeCheckError(f"Cannot assign a list to a variable.", lineNumber)

                    scopes.updateVariable(firstOperand, createDummyObject(secondOperandType))
                    return secondOperandType
                
                case "^":
                    if not checkTypeTwo(firstOperandType, secondOperandType, Number, Number):
                        typeCheckError(errorString, lineNumber)
                    if (issubclass(firstOperandType, Float) or issubclass(secondOperandType, Float)):
                        return Float
                    else:
                        return Int


        case UnOp(lineNumber, operator, operand):   
            opearandType = typecheck(operand, scopes)
            
            if (operator not in UNARY_OPERATORS):
                typeCheckError(f"Unary Operator {operator} not reconized", lineNumber)
            
            match operator:
                case "-":
                    if not issubclass(opearandType, Number):
                        typeCheckError(f"Operator {operator} is not defined for data type {opearandType.__name__}", lineNumber)
                    elif (isinstance(opearandType, Float)):
                        return Float
                    else:
                        return Int
                case "~":
                    if not issubclass(opearandType, Bool):
                        typeCheckError(f"Operator {operator} is not defined for data type {opearandType.__name__}", lineNumber)
                    return Bool

        case Declare(lineNumber, var, value, dtype, isConst):
            if (not isinstance(var, Variable)):
                raise Exception("RHS of declaration must be of type \'Variable\'")

            # Make sure all the elements of the list are of the type zList.dtype
            if (dtype == zList):
                tempval=value
                value = typecheckList(value, lineNumber, scopes)
                scopes.declareVariable(var, tempval, dtype, isConst)
            else:
                # Evaluating the expression before declaration
                
                value = typecheck(value, scopes)
                
                # Declaring
                scopes.declareVariable(var, createDummyObject(value), dtype, isConst)
            return dtype

        case Slice(lineNumber, value_, first, second):       #checking value_ is string 
            tc = typecheck(value_, scopes)
            tf = typecheck(first, scopes)
            ts = typecheck(second, scopes)
            if (not(issubclass(tc, Str | zList))):
                typeCheckError(f"Slice operation not defined for {type(tc).__name__}", lineNumber)
            if not (issubclass(tf, Int) or issubclass(ts, Int)):
                typeCheckError(f"Slice indices must be of {Int} type", lineNumber)
            if(issubclass(ts,nil) and issubclass(tc,zList)):
                element_type = scopes.getVariable(value_).dtype
                return element_type
            return tc

        case While(lineNumber, condition, block) :            #checking while condition data type
            tc = typecheck(condition, scopes)
            if (not(issubclass(tc, AST))):
                raise Exception("Arguments passed to While block must be of 'AST' type")
            return typecheck(block, scopes)
        
        case If (lineNumber, condition, ifBlock, elseBlock): #checking if condition data type
            tc = typecheck(condition, scopes)
            if (not (issubclass(tc, AST))):
                raise Exception("Arguments passed to If block must be of 'AST' type")
            return typecheck(ifBlock, scopes) | typecheck(elseBlock, scopes)

        case For(lineNumber, initial,condition,block):
            scopes.beginScope()
            
            tc1 = typecheck(initial, scopes)
            if(not(issubclass(tc1,AST))):
                raise Exception("Arguments passes to For initial must be of 'AST' type")
            tc = typecheck(condition, scopes)
            if(not( issubclass(tc,AST))):
                raise Exception("Arguments passes to For condition must be of 'AST' type")
            retType = typecheck(block, scopes)
            
            scopes.endScope()
            return retType

        case Seq(lines):
            ret = nil
            for line in lines:
                ret = typecheck(line, scopes)
            return ret
        
        case PRINT(lineNumber, exps, sep,end):
            sep = typecheck(sep, scopes)
            end = typecheck(end, scopes)
            for exp in exps:
                exp = typecheck(exp, scopes)
                if (not issubclass(exp, AST)):
                    raise Exception(f"Invalid expression {exp} in PRINT")
                if (not issubclass(sep, Str)):
                    typeCheckError(f"Invalid separator {sep} in PRINT at {lineNumber}")
                if (not issubclass(end, Str)):
                    typeCheckError(f"Invalid end {end} in PRINT at {lineNumber}")
            return nil
        
        case list_append(lineNumber, element, list_name):
            var_type = scopes.getVariableType(list_name)
            lIsConst = scopes.getVariableIsConst(list_name)
            lType = scopes.getVariable(list_name).dtype
            element=typecheck(element,scopes)
            if not(issubclass(var_type, zList)):
                typeCheckError(f"Cannot append an element of type {(element)} to a {var_type}.", lineNumber)
            elif lIsConst:
                typeCheckError(f"Cannot append an element to a constant list.", lineNumber, "constError")
            elif not (issubclass(element, lType)):
                typeCheckError(f"Cannot append an element of type {(element)} to a list of type {lType}.", lineNumber)
            return nil
        
        case list_remove(lineNumber, index, list_name):
            var_type = scopes.getVariableType(list_name)
            lIsConst = scopes.getVariableIsConst(list_name)
            if not(issubclass(var_type, zList)):
                typeCheckError(f"Cannot remove an element from {var_type}.", lineNumber)
            elif lIsConst:
                typeCheckError(f"Cannot remove an element from a constant list.", lineNumber, "integrityError")
            return var_type
            
        case list_len(lineNumber, l):
            l = typecheck(l, scopes)
            if not(issubclass(l, zList|Str)):
                typeCheckError(f"length attribute not defined for variable of type  {l.__name__}.", lineNumber)
            return Int
        
        case list_pop(lineNumber, list_name):
            var_type = scopes.getVariableType(list_name)
            lIsConst = scopes.getVariableIsConst(list_name)
            if not(issubclass(var_type, zList)):
                typeCheckError(f"Cannot popout an element from {var_type}.", lineNumber)
            elif lIsConst:
                typeCheckError(f"Cannot popout an element from a constant list.", lineNumber, "constError")
            return var_type
        
        case list_insert(lineNumber, index, element, list_name):
            var_type = scopes.getVariableType(list_name)
            lIsConst = scopes.getVariableIsConst(list_name)
            lType = scopes.getVariable(list_name).dtype
            element=typecheck(element, scopes)
            index=typecheck(index, scopes)
            if not(issubclass(var_type, zList)):
                typeCheckError(f"Cannot append an element of type {element} to a {var_type}.", lineNumber)
            elif lIsConst:
                typeCheckError(f"Cannot append an element to a constant list.", lineNumber, "constError")
            elif not (issubclass(index, Int)):
                typeCheckError(f"index must be an integer.", lineNumber)
            elif not (issubclass(element, lType)):
                typeCheckError(f"Cannot append an element of type {element} to a list of type {lType}.", lineNumber)
            return nil
         
        case DeclareFun(lineNumber, Variable(_, name, id) as f, return_type, params_type, params, body):
            # Declaring the function in the current scope
            scopes.declareFun(f, FnObject(params_type, params, body, return_type)) 

            # Strategy to type check the body

            # 1. begin a new scope
            scopes.beginScope()

            # 2. Initialize all the params using a dummy object
            for param, param_type in zip(params, params_type):
                scopes.declareVariable(param, createDummyObject(param_type), param_type, False)

            # 3. type check the body
            retType = typecheck(body, scopes)

            # 4. make sure that the return types are the same
            if (not(issubclass(retType, return_type) and issubclass(retType, return_type))):
                typeCheckError(f"Not matching the expected return type of the function", lineNumber)
            
            # 5. return nil as declaration statements have no return type
            return nil
        
        case FunCall(lineNumber, Variable(_, name, id) as f, args): 
            # Get the function object
            fn = scopes.getVariable(f)
            
            # Generate the type of arguments
            argv = []
            for arg in args:
                argv.append(typecheck(arg, scopes))
            
            # Only typechecking the param type and the argument types
            p_types = fn.params_types
            for i in range(len(p_types)):
                if (not(issubclass(p_types[i],(argv[i])))):
                    raise typeCheckError(f"{i+1}th Argument passed to the function is of invalid type", lineNumber)

            # Returning the return type of the function
            return fn.return_type
        
        case Return(lineNumber, exp):
            exp = typecheck(exp, scopes)
            return exp
        
        case Block(blockStatements):
            # Return the type of the last statement in the seq in block
            return typecheck(blockStatements, scopes)
        
        case _ as v:
            raise Exception(f"Got {v}, Invalid Expression|Statement")
