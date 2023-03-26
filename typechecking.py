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
    if type_ == Int or type_ == Float or type_ == Bool or type_ == Str:
        return type_(None)
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
        case BinOp(operator, firstOperand, secondOperand):
            # Getting the operand types
            firstOperandType = typecheck(firstOperand, scopes)
            secondOperandType = typecheck(secondOperand, scopes)
            
            # Checking if the operator is defined
            if (operator.val not in BINARY_OPERATORS):
                typeCheckError(f"Binary Operator {operator} not reconized", operator.lineNumber)
            
            # General BinOp type error string
            errorString = f"Operator {operator} not defined between data types {firstOperandType.__name__} and {secondOperandType.__name__}"

            match operator.val:
                case  "+":
                    if (issubclass(firstOperandType, Str) and not checkTypeTwo(firstOperandType, secondOperandType, Str, Str)):
                        typeCheckError(errorString, operator.lineNumber)
                    elif (issubclass(firstOperandType, Number) and not checkTypeTwo(firstOperandType, secondOperandType, Number, Number)):
                        typeCheckError(errorString, operator.lineNumber)
                    if (issubclass(firstOperandType, Float) or issubclass(secondOperandType, Float)):
                        return Float
                    else:
                        return Int
                    
                case  "-":
                    if not checkTypeTwo(firstOperandType, secondOperandType, Number, Number):
                        typeCheckError(errorString, operator.lineNumber)
                    
                    if (issubclass(firstOperandType, Float) or issubclass(secondOperandType, Float)):
                        return Float
                    else:
                        return Int

                case "/":
                    if not checkTypeTwo(firstOperandType, secondOperandType, Number, Number):
                        typeCheckError(errorString, operator.lineNumber)
                    return Float
                
                case "*":
                    if (issubclass(firstOperandType,Str) and issubclass(secondOperandType, Int)):
                        return Str

                    elif (issubclass(firstOperandType,Int) and issubclass(secondOperandType,Str)):
                        return Str
                    elif not checkTypeTwo(firstOperandType, secondOperandType, Number, Number):
                        typeCheckError(errorString, operator.lineNumber)
                    else:
                        if (issubclass(firstOperandType, Float) | issubclass(secondOperandType, Float)):
                            return Float
                        else:
                            return Int
                
                case "//" :
                    if not checkTypeTwo(firstOperandType, secondOperandType, Number, Number):
                        typeCheckError(errorString, operator.lineNumber)
                    return Int
                
                case "%" | "<<" | ">>" | "&" | "|":
                    if not checkTypeTwo(firstOperandType, secondOperandType, Int, Int):
                        typeCheckError(errorString, operator.lineNumber)
                    return Int
                
                
                case "<=" | "<" | "==" | ">" | ">=" | "!=":
                    if not checkSameType(firstOperandType, secondOperandType):
                        typeCheckError(errorString, operator.lineNumber)
                    return Bool
                
                case "&&" | "||": 
                    if not checkTypeTwo(firstOperandType, secondOperandType, AST, AST):
                        typeCheckError(errorString, operator.lineNumber)
                    return Bool
                
                case "=":                    
                    # Prevent assignment for lists (for now)
                    if (issubclass(secondOperandType, zList)):
                        typeCheckError(f"Cannot assign a list to a variable.", operator.lineNumber)

                    scopes.updateVariable(firstOperand.name, createDummyObject(secondOperandType))
                    return secondOperandType

        case UnOp(operator, operand):   
            opearandType = typecheck(operand, scopes)
            
            if (operator.val not in UNARY_OPERATORS):
                typeCheckError(f"Unary Operator {operator} not reconized", operator.lineNumber)
            
            match operator.val:
                case "-":
                    if not issubclass(opearandType, Number):
                        typeCheckError(f"Operator {operator} is not defined for data type {opearandType.__name__}", operator.lineNumber)
                    elif (isinstance(opearandType, Float)):
                        return Float
                    else:
                        return Int
                case "~":
                    if not issubclass(opearandType, Bool):
                        typeCheckError(f"Operator {operator} is not defined for data type {opearandType.__name__}", operator.lineNumber)
                    return Bool

        case Declare(var, value, dtype, isConst):
            if (not isinstance(var, Identifier)):
                raise Exception("RHS of declaration must be of type \'Identifier\'")

            # Make sure all the elements of the list are of the type zList.dtype
            if (dtype == zList):
                tempval=value
                value = typecheckList(value, var.lineNumber, scopes)
                scopes.declareVariable(var, tempval, dtype, isConst)
            else:
                # Evaluating the expression before declaration
                value = typecheck(value, scopes)
                # Declaring
                scopes.declareVariable(var, createDummyObject(value), dtype, isConst)
            return dtype

        case Slice(value_, first, second):       #checking value_ is string 
            tc = typecheck(value_, scopes)
            tf = typecheck(first, scopes)
            ts = typecheck(second, scopes)
            if (not(issubclass(tc, Str | zList))):
                typeCheckError("First argument passed to Slice must be of {Str} | {zList} type", None)
            if not (issubclass(tf, Int) or issubclass(ts, Int)):
                typeCheckError("Second and third arguments passed to Slice must be of {Int} type", None)
            return tc

        case While(condition,block) :            #checking while condition data type
            tc = typecheck(condition, scopes)
            if (not(issubclass(tc, AST))):
                raise Exception("Arguments passed to While block must be of 'AST' type")
            return typecheck(block, scopes)
        
        case If (condition, ifBlock, elseBlock): #checking if condition data type
            tc = typecheck(condition, scopes)
            if (not (issubclass(tc, AST))):
                raise Exception("Arguments passed to If block must be of 'AST' type")
            return typecheck(ifBlock, scopes) | typecheck(elseBlock, scopes)

        case For(initial,condition,block):
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
            element=typecheck(element,scopes)
            if not(issubclass(var_type, zList)):
                typeCheckError(f"Cannot append an element of type {(element)} to a {var_type}.", None)
            elif lIsConst:
                typeCheckError(f"Cannot append an element to a constant list.", None, "constError")
            elif not (issubclass(element, lType)):
                typeCheckError(f"Cannot append an element of type {(element)} to a list of type {lType}.", None)
            return nil
        
        case list_remove(index, list_name):
            var_type = scopes.getVariableType(list_name.val)
            lIsConst = scopes.getVariableIsConst(list_name.val)
            if not(issubclass(var_type, zList)):
                typeCheckError(f"Cannot remove an element from {var_type}.", None)
            elif lIsConst:
                typeCheckError(f"Cannot remove an element from a constant list.", None, "constError")
            return var_type
            
        case list_len(l):
            l = typecheck(l, scopes)
            if not(issubclass(l, zList)):
                typeCheckError(f"Cannot remove an element from {l}.", None)
            return Int
        
        case list_insert(index, element, list_name):
            var_type = scopes.getVariableType(list_name.val)
            lIsConst = scopes.getVariableIsConst(list_name.val)
            lType = scopes.getVariable(list_name.val).dtype
            element=typecheck(element, scopes)
            index=typecheck(index, scopes)
            if not(issubclass(var_type, zList)):
                typeCheckError(f"Cannot append an element of type {element} to a {var_type}.", None)
            elif lIsConst:
                typeCheckError(f"Cannot append an element to a constant list.", None, "constError")
            elif not (issubclass(index, Int)):
                typeCheckError(f"index must be an integer.", None)
            elif not (issubclass(element, lType)):
                typeCheckError(f"Cannot append an element of type {element} to a list of type {lType}.", None)
            return nil
         
        case DeclareFun(Identifier(lineNumber, _) as f, return_type, params_type, params, body):
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
                typeCheckError(f"Not returning the expected return type of the function", f.lineNumber)
            
            # 5. return nil as declaration statements have no return type
            return nil
        
        case FunCall(Identifier(lineNumber, _) as f, args): 
            # Get the function object
            fn = scopes.getVariable(f.val)
            
            # Generate the type of arguments
            argv = []
            for arg in args:
                argv.append(typecheck(arg, scopes))
            
            # Only typechecking the param type and the argument types
            p_types = fn.params_types
            for i in range(len(p_types)):
                if (not(issubclass(p_types[i],(argv[i])))):
                    raise Exception(f" {i+1}th Argument passed to the function is of invalid type")

            # Returning the return type of the function
            return fn.return_type
        
        case Block(blockStatements):
            # Return the type of the last statement in the seq in block
            return typecheck(blockStatements, scopes)
        
        case _:
            raise Exception("Type checking failed.")
