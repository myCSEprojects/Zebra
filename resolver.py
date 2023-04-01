from sim import *

@dataclass
class ResolverScopes:
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
        
    def declareFun(self, name: str, var: Variable, fn_object: FnObject):
        '''
        Declares the function in the current scope as the variable f
        '''
        assert(len(self.stack) != 0)

        # Avoiding redeclarations in the same scope
        if name in self.stack[-1]:
            resolveError(f"Redeclaring already declared function {name}", var.lineNumber)
        self.stack[-1][name] = var  

    def declareVariable(self, name: str, var: Variable):
        '''
        Only declares a variable in the current scope
        '''
        assert(len(self.stack) != 0)

        # Avoiding redeclaration in the same scope
        if name in self.stack[-1]:
            resolveError(f"Redeclaring already declared variable {name}", var.lineNumber)
        
        self.stack[-1][name] = var


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
        case Int() | Float() | Bool() | Str() | nil() | zList() as literal:
            return literal
        
        case Variable(lineNumber, name, id) as v:
            # Getting the resolved variable
            referencingVariable = scopes.getVariable(name, lineNumber)
            # Setting the exact line number of the variable
            resolvedVariable = Variable(lineNumber, name, referencingVariable.id)
            return resolvedVariable
        
        case Declare(lineNumber, var, value, dtype, isConst):
            # Resolving the value
            resolvedValue = resolve(value, scopes)
            # Declaring the variable
            scopes.declareVariable(var.name, var)
            return Declare(lineNumber, var, resolvedValue, dtype, isConst)
        
        case DeclareFun(lineNumber, var, return_type, params_type, params, body):
            # Declaring the function
            scopes.declareFun(var.name, var, FnObject(return_type, params_type, params, body))
            scopes.beginScope()
            # Declaring the parameters
            for param in params:
                scopes.declareVariable(param.name, param)
            # Resolving the body
            resolvedBody = resolve(body, scopes)
            scopes.endScope()
            # Resolving the body
            return DeclareFun(lineNumber, var, return_type, params_type, params, resolvedBody)
        
        case FunCall(lineNumber, var, args):
            # Resolving the function variable
            resolvedVar = resolve(var, scopes)
            # Resolving the arguments
            resolvedArgs = [resolve(arg, scopes) for arg in args]
            return FunCall(lineNumber, resolvedVar, resolvedArgs)
        
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
        
        case list_append(lineNumber, element, var):
            # Resolving the element
            resolvedElement = resolve(element, scopes)
            # Resolving the variable
            resolvedVar = resolve(var, scopes)
            return list_append(lineNumber, resolvedElement, resolvedVar)
        
        case list_remove(lineNumber, index , var):
            # Resolving the index
            resolvedIndex = resolve(index, scopes)
            # Resolving the variable
            resolvedVar = resolve(var, scopes)
            return list_remove(lineNumber, resolvedIndex, resolvedVar)
        
        case list_len(lineNumber, var):
            # Resolving the variable
            resolvedVar = resolve(var, scopes)
            return list_len(lineNumber, resolvedVar)
        
        case list_insert(lineNumber, index, element, var):
            # Resolving the index
            resolvedIndex = resolve(index, scopes)
            # Resolving the element
            resolvedElement = resolve(element, scopes)
            # Resolving the variable
            resolvedVar = resolve(var, scopes)
            return list_insert(lineNumber, resolvedIndex, resolvedElement, resolvedVar)