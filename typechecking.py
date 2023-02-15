from sim import *

@dataclass
class TypecheckerScopes:
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
    
    def declareVariable(self, var: Variable, rtype: 'AST', ltype:'AST', isConst: bool):
        '''
        Only declares a variable in the current scope
        '''
        assert(len(self.stack) != 0)

        # Avoiding redeclaration in the same scope
        if var.name in self.stack[-1]:
            InvalidProgram(Exception(f"Redeclaring already declared variable {var.name}"))
        print(rtype, ltype)
        if (rtype != ltype):
            InvalidProgram(Exception(f"Cannot initialize {ltype} with Literal of dtype {rtype}."))

        self.stack[-1][var.name] = [ltype, isConst]
    
    def updateVariable(self, name: str, rtype: AST):
        for i in range(len(self.stack)-1, -1, -1):
            if name in self.stack[i]:
                if (self.stack[i][name][1] == True):
                    InvalidProgram(Exception(f"Cannot Update const Variable {name}"))
                if (rtype != self.stack[i][name][0]):
                    InvalidProgram(Exception(f"Cannot assign {rtype} to {self.stack[i][name][0]}"))
                return
        
        InvalidProgram(Exception(f"Could not find the variable {name}."))

    def getVariable(self, name: str):
        for i in range(len(self.stack)-1, -1, -1):
            if name in self.stack[i]:
                return self.stack[i][name][0]
        
        InvalidProgram(Exception(f"Could not resolve the variable {name}."))

Number = Int | Float

# Since we don't have variables, scopes is not needed.
def typecheck(program: AST, scopes = None):
    if (scopes == None):
        scopes = TypecheckerScopes()
    match program:
        case Float(): 
            return Float
        case Int(): 
            return Int
        case Bool(): 
            return Bool
        case Variable(name):
            return scopes.getVariable(name)
        case Str():
            return Str
        case nil():
            return nil
        case BinOp(operator, left, right):
            firstOperand = typecheck(left, scopes)
            secondOperand = typecheck(right, scopes)
            
            if (operator not in BINARY_OPERATORS):
                InvalidProgram(Exception(f"Operator {operator} not reconized"))
            
            match operator:
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
                    BinOp.checkType(operator, left, right, Variable, AST)
                    scopes.updateVariable(left.name, secondOperand)
                    BinOp.checkSameType(operator, firstOperand, secondOperand)
                    return secondOperand

        case UnOp(operator, operand):   
            ot = typecheck(operand, scopes)
            match operator:
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
            if (not isinstance(var, Variable)):
                InvalidProgram(Exception("RHS of declaration must be of type \'Variable\'"))
            
            # Evaluating the expression before declaration
            value = typecheck(value, scopes)

            # Declaring
            scopes.declareVariable(var, dtype, value, isConst)
            return value

        case Slice(value_, first, second):       #checking value_ is string 
            tc = typecheck(value_, scopes)
            if (not(issubclass(tc, Str))):
                InvalidProgram(Exception("Arguments passed to Slice must be of 'Str' type"))
            return Str

        case While(condition,block) :            #checking while condition data type
            tc = typecheck(condition, scopes)
            if (not(issubclass(tc, AST))):
                InvalidProgram(Exception("Arguments passed to While block must be of 'AST' type"))
            return nil
        
        case If (condition, ifBlock, elseBlock): #checking if condition data type
            tc = typecheck(condition, scopes)
            if (not (issubclass(tc, AST))):
                InvalidProgram(Exception("Arguments passed to If block must be of 'AST' type"))
            return nil

        case For(initial,condition,block):
            tc1 =typecheck(initial, scopes)
            if(not(issubclass(tc1,AST))):
                InvalidProgram(Exception("Arguments passes to For initial must be of 'AST' type"))
            tc = typecheck(condition, scopes)
            if(not( issubclass(tc,AST))):
                InvalidProgram(Exception("Arguments passes to For condition must be of 'AST' type"))
            return nil

        case Seq(lines):
            ret = nil()
            for line in lines:
                ret = typecheck(line, scopes)
            return ret
        case PRINT(exps):
            for exp in exps:
                if (not isinstance(exp, AST)):
                    InvalidProgram(Exception(f"Invalid expression {exp} in PRINT"))
            return nil
        case _:
            InvalidProgram(Exception("Type checking failed."))
