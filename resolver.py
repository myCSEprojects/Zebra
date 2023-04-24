from sim import *

@dataclass
class ResolverScopes:
    '''
    Scopes storing the stack of environments
    '''
    stack: List[Dict[Variable, "AST"]]
    localIDStack: List[int]

    def __init__(self, stack: List[Dict[Variable, "AST"]] = None):
        if (stack == None):
            self.stack = [dict()]
            self.localIDStack = [0]
        else:
            self.stack = stack
            self.localIDStack = [0]
    
    def current_fdepth(self):
        return len(self.localIDStack) - 1

    def beginFun(self):
        self.localIDStack.append(0)
    
    def endFun(self):
        self.localIDStack.pop()

    def beginScope(self):
        self.stack.append({})
    
    def endScope(self):
        assert(len(self.stack) != 0)
        self.stack.pop()
        
    def declareFun(self, name: str, var: Variable, fn_object: FnObject):
        '''
        Declares the function in the current scope as the variable f
        '''
        assert(len(self.stack) != 0)

        # Avoiding redeclarations in the same scope
        if name in self.stack[-1]:
            resolveError(f"Redeclaring already declared function {name}", var.lineNumber)
        newVar = Variable(var.lineNumber,var.name, var.id, self.localIDStack[-1], self.current_fdepth(), 0)
        self.localIDStack[-1] += 1
        self.stack[-1][name] = newVar
        return newVar

    def declareVariable(self, name: str, var: Variable):
        '''
        Only declares a variable in the current scope
        '''
        assert(len(self.stack) != 0)

        # Avoiding redeclaration in the same scope
        if name in self.stack[-1]:
            resolveError(f"Redeclaring already declared variable {name}", var.lineNumber)
        newVar = Variable(var.lineNumber,
                          var.name, 
                          var.id, 
                          self.localIDStack[-1], 
                          self.current_fdepth(), 
                          0)
        self.localIDStack[-1] += 1
        self.stack[-1][name] = newVar  
        return newVar


    def getVariable(self, name: str, lineNumber: int):
        '''
        Utility to get the variable in the closest scope
        '''
        for scope in reversed(self.stack):
            if name in scope:
                return scope[name]
        resolveError(f"Could not resolve the variable {name}", lineNumber)

def resolve(program: AST, scopes : ResolverScopes = None):
    '''
    Resolves the given program AST
    '''
    if scopes == None:
        scopes = ResolverScopes()
    
    match program:

        case Int() | Float() | Bool() | Str() | nil() as literal:
            return literal
        
        case zArray():
            # Resolving the elements
            for i in range(len(program.elements)):
                program.elements[i] = resolve(program.elements[i], scopes)
            return program
        
        case Variable(lineNumber, name, id) as v:
            # Getting the resolved variable
            referencingVariable = scopes.getVariable(name, lineNumber)
            # Setting the exact line number of the variable
            resolvedVariable = Variable(lineNumber, 
                                        name, 
                                        referencingVariable.id, 
                                        referencingVariable.localID,
                                        referencingVariable.fdepth,
                                        scopes.current_fdepth()-referencingVariable.fdepth)
            return resolvedVariable
        
        case Declare(lineNumber, var, value, dtype, isConst):
            # Resolving the value
            resolvedValue = resolve(value, scopes)
            # Declaring the variable
            newVar = scopes.declareVariable(var.name, var)
            # Resolving the data type
            if ((not isinstance(dtype, type)) and isinstance(dtype, instanceType)):
                dtype = instanceType(scopes.getVariable(dtype.name.name, lineNumber))
            return Declare(lineNumber, newVar, resolvedValue, dtype, isConst)
        
        case DeclareClass(lineNumber, var, stmts, thisID):
            # Declaring the class
            newVar = scopes.declareVariable(var.name, var)
            # Resolving the statements
            scopes.beginScope()
            # Declaring the this variable
            scopes.declareVariable("this", Variable(lineNumber, "this", thisID, None, None, None))
            for methodName in stmts:
                
                stmts[methodName] = resolve(stmts[methodName], scopes)
            scopes.endScope()
            return DeclareClass(lineNumber, newVar , stmts, thisID)

        case DeclareFun(lineNumber, var, return_type, params_type, params, body, function_type):
            # Declaring the function
            newVar = scopes.declareFun(var.name, var, FnObject(function_type, return_type, params_type, params, body))
            scopes.beginScope()
            scopes.beginFun()
            # Declaring the parameters
            for i in range(len(params)):
                params[i] = scopes.declareVariable(params[i].name, params[i])
            for i in range(len(params_type)):
                if ((not isinstance(params_type[i], type)) and isinstance(params_type[i], instanceType)):
                    params_type[i] = instanceType(scopes.getVariable(params_type[i].name.name, lineNumber))
            # Resolving the body
            resolvedBody = resolve(body, scopes)
            scopes.endFun()
            scopes.endScope()
            return DeclareFun(lineNumber, newVar, return_type, params_type, params, resolvedBody, function_type)
        
        case Get(lineNumber, var, name):
            resolvedVar = resolve(var, scopes)
            return Get(lineNumber, resolvedVar, name)
        
        case Set(lineNumber, var, name, value):
            resolvedVar = resolve(var, scopes)
            resolvedValue = resolve(value, scopes)
            return Set(lineNumber, resolvedVar, name, resolvedValue)
        
        case AtIndex(lineNumber, var, index):
            resolvedVar = resolve(var, scopes)
            resolvedIndex = resolve(index, scopes)
            return AtIndex(lineNumber, resolvedVar, resolvedIndex)
        
        case SetAtIndex(lineNumber, var, index, value):
            resolvedVar = resolve(var, scopes)
            resolvedIndex = resolve(index, scopes)
            resolvedValue = resolve(value, scopes)
            return SetAtIndex(lineNumber, resolvedVar, resolvedIndex, resolvedValue)

        case FunCall(lineNumber, var, args):
            # Resolving the function variable
            resolvedVar = resolve(var, scopes)
            # Resolving the arguments
            resolvedArgs = [resolve(arg, scopes) for arg in args]
            return FunCall(lineNumber, resolvedVar, resolvedArgs)
        
        case Return(lineNumber, value):
            # Resolving the value
            resolvedValue = resolve(value, scopes)
            return Return(lineNumber, resolvedValue)
        
        case Block(blockStatements):
            # Resolving the block statements
            scopes.beginScope()
            resolvedBlockStatements = Seq([resolve(statement, scopes) for statement in blockStatements.lines])
            scopes.endScope()
            return Block(resolvedBlockStatements)
        
        case If(lineNumber, condition, ifBlock, elseBlock):
            # Resolving the condition
            resolvedCondition = resolve(condition, scopes)
            # Resolving the if block
            resolvedIfBlock = resolve(ifBlock, scopes)
            # Resolving the else block
            resolvedElseBlock = resolve(elseBlock, scopes)
            return If(lineNumber, resolvedCondition, resolvedIfBlock, resolvedElseBlock)
        
        case While(lineNumber, condition, block):
            # Resolving the condition
            resolvedCondition = resolve(condition, scopes)
            # Resolving the block
            resolvedBlock = resolve(block, scopes)
            return While(lineNumber, resolvedCondition, resolvedBlock)
        
        case Seq(lines):
            # Resolving the lines
            resolvedLines = [resolve(line, scopes) for line in lines]
            return Seq(resolvedLines)
        
        case This(lineNumber, id):
            referencingVariable = scopes.getVariable("this", lineNumber)
            resolvedThis = This(lineNumber, referencingVariable.id, None, None, None)
            return resolvedThis

        case PRINT(lineNumber, print_stmts, sep,end):
            # Resolving the print statement
            resolvedPrintStmt = [resolve(print_stmt, scopes) for print_stmt in print_stmts]
            resolvedSep = resolve(sep, scopes)
            resolvedEnd = resolve(end, scopes)
            return PRINT(lineNumber, resolvedPrintStmt, resolvedSep, resolvedEnd)
        
        case BinOp(lineNumber, op, left, right):
            # Resolving the left and right
            resolvedLeft = resolve(left, scopes)
            resolvedRight = resolve(right, scopes)
            return BinOp(lineNumber, op, resolvedLeft, resolvedRight)
        
        case UnOp(lineNumber, op, expr):
            # Resolving the expression
            resolvedExpr = resolve(expr, scopes)
            return UnOp(lineNumber, op, resolvedExpr)
        
        case For(lineNumber, initial,condition,block):
            scopes.beginScope()
            # Resolving the initial
            resolvedInitial = resolve(initial, scopes)
            # Resolving the condition
            resolvedCondition = resolve(condition, scopes)
            # Resolving the block
            resolvedBlock = resolve(block, scopes)
            scopes.endScope()
            return For(lineNumber, resolvedInitial, resolvedCondition, resolvedBlock)
        
        case Slice(lineNumber, value_, first, second):
            # Resolving the value
            resolvedValue = resolve(value_, scopes)
            # Resolving the first
            resolvedFirst = resolve(first, scopes)
            # Resolving the second
            resolvedSecond = resolve(second, scopes)
            return Slice(lineNumber, resolvedValue, resolvedFirst, resolvedSecond)
        
        case array_append(lineNumber, element, var):
            # Resolving the element
            resolvedElement = resolve(element, scopes)
            # Resolving the variable
            resolvedVar = resolve(var, scopes)
            return array_append(lineNumber, resolvedElement, resolvedVar)
        
        case array_remove(lineNumber, index , var):
            # Resolving the index
            resolvedIndex = resolve(index, scopes)
            # Resolving the variable
            resolvedVar = resolve(var, scopes)
            return array_remove(lineNumber, resolvedIndex, resolvedVar)
        
        case array_len(lineNumber, var):
            # Resolving the variable
            resolvedVar = resolve(var, scopes)
            return array_len(lineNumber, resolvedVar)
        
        case array_insert(lineNumber, index, element, var):
            # Resolving the index
            resolvedIndex = resolve(index, scopes)
            # Resolving the element
            resolvedElement = resolve(element, scopes)
            # Resolving the variable
            resolvedVar = resolve(var, scopes)
            return array_insert(lineNumber, resolvedIndex, resolvedElement, resolvedVar)
        
        case array_pop(lineNumber, var):
            # Resolving the variable
            resolvedVar = resolve(var, scopes)
            return array_pop(lineNumber, resolvedVar)
        
