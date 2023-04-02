from fractions import Fraction
from dataclasses import dataclass
from typing import Optional, NewType
from sim import *
from lexer import *
from error import ParseError, ParseException, TokenException
import pprint

# Global value denoting if the Parse Error occured
isParseError = False

id: Int = 0        # Global ID useful for the resolver pass

def generate_id():
    global id
    id += 1
    return id

# Data Types dictionary
dtypes_dict = {
    "int" : Int, 
    "float": Float, 
    "string": Str, 
    "boolean": Bool
}

def get_AST_type(tk: Token):
    '''
    Utility to convert token types to AST values
    '''
    match tk:
        case Integer(lineNumber, val):
            return Int(val)
        case Flt(lineNumber, val):
            return Float(val)
        case Boolean(lineNumber, val):
            return Bool(val)
        case String(lineNumber, val):
            return Str(val)
        case Identifier(lineNumber, val):
            return Variable(val)
        case _:
            return nil()

@dataclass
class Parser:
    
    lexer: Lexer # Lexer to produce the tokens

    def from_lexer(lexer):
        return Parser(lexer)
    
    def parse_block(self):
        self.lexer.match(Operator(0,"{"))
        block_seq = []
        while(self.lexer.peek_token().val != "}" ):
            t = self.parse_declare()
            block_seq.append(t)
        self.lexer.match(Operator(0,"}"))
        return Block(Seq(block_seq))
    

    def parse_if(self):
        lineNumber = self.lexer.peek_token().lineNumber
        self.lexer.match(Keyword(0,"if"))
        self.lexer.match(Operator(0,"("))
        c = self.parse_expr()
        self.lexer.match(Operator(0,")"))
        if_block = self.parse_block()
        if(self.lexer.peek_token().val != "else"):
            return If(c,if_block,None)
        self.lexer.match(Keyword(0,"else"))
        if (self.lexer.peek_token().val == "if") :
            else_block = self.parse_if()
        else :
            else_block = self.parse_block()
        
        return If(lineNumber, c,if_block, else_block)

    def parse_for(self):
        lineNumber = self.lexer.peek_token().lineNumber
        self.lexer.match(Keyword(0, "for"))
        self.lexer.match(Operator(0, "("))
        bf = self.lexer.peek_token()
        initial = nil()
        if(self.lexer.peek_token().val in dtypes):
            initial = self.parse_vardec()
        elif (bf.val == ";") :
            self.lexer.advance()
        else:
            initial = self.parse_expr_stmt()

        condition = self.parse_expr()
        self.lexer.match(Operator(0, ";"))
        bf = self.lexer.peek_token()
        
        order = nil()
        if (bf.val != ")") :
            order = self.parse_expr()

        self.lexer.match(Operator(0, ")"))

        for_block = self.parse_block()
        if (order != nil()):
            for_block.blockStatements.lines.append(order)
        return For(lineNumber, initial, condition, for_block)
        
    
    def parse_while(self):
        lineNumber = self.lexer.peek_token().lineNumber
        self.lexer.match(Keyword(0, "while"))
        self.lexer.match(Operator(0, "("))
        c = self.parse_expr()
        self.lexer.match(Operator(0, ")"))
        w_block = self.parse_block()
        return While(lineNumber, c, w_block)
    
    def parse_print(self):
        lineNumber = self.lexer.peek_token().lineNumber
        self.lexer.match(Keyword(0, "zout"))
        self.lexer.match(Operator(0, "("))
        pseq=[]
        pseq.append(self.parse_expr())
        sep_ = Str(" ")
        end_ = Str("\n")
        while(self.lexer.peek_token().val != ")"):
            self.lexer.match(Operator(0, ","))
            if (self.lexer.peek_token().val == "sep"):
                self.lexer.match(Keyword(0, "sep"))
                self.lexer.match(Operator(0, "="))
                sep = self.lexer.peek_token()
                if not isinstance(sep, String):
                    ParseError(self, f"Expected a string", sep.lineNumber)
                self.lexer.advance()
                sep_ = Str(sep.val)
                
            elif (self.lexer.peek_token().val == "end"):
                self.lexer.match(Keyword(0, "end"))
                self.lexer.match(Operator(0, "="))
                end = self.lexer.peek_token()
                if not isinstance(end, String):
                    ParseError(self, f"Expected a string", end.lineNumber)
                self.lexer.advance()
                end_ = Str(end.val)
                
            else:
                t=self.parse_expr()
                pseq.append(t)
        self.lexer.match(Operator(0, ")"))
        self.lexer.match(Operator(0, ";"))
        return PRINT(lineNumber, pseq,sep_,end_)

    def parse_append(self):
        lineNumber = self.lexer.peek_token().lineNumber
        self.lexer.match(Keyword(0, "append"))
        self.lexer.match(Operator(0,"("))
        ele=self.parse_expr()
        self.lexer.match(Operator(0,","))
        l=self.lexer.peek_token()
        if not isinstance(l, Identifier):
            ParseError(self, f"Expected an identifier", l.lineNumber)
        self.lexer.advance()
        var = Variable(l.lineNumber, l.val, generate_id())
        self.lexer.match(Operator(0,")"))
        self.lexer.match(Operator(0,";"))
        return list_append(lineNumber, ele, var)
    
    def parse_remove(self):
        lineNumber = self.lexer.peek_token().lineNumber
        self.lexer.match(Keyword(0, "remove"))
        self.lexer.match(Operator(0, "("))
        index=self.parse_expr()
        self.lexer.match(Operator(0,","))
        l=self.lexer.peek_token()
        if not isinstance(l, Identifier):
            ParseError(self, f"Expected an identifier", l.lineNumber)
        self.lexer.advance()
        var = Variable(l.lineNumber, l.val, generate_id())
        self.lexer.match(Operator(0,")"))
        self.lexer.match(Operator(0,";"))
        return list_remove(lineNumber, index, var)
    
    def parse_len(self):
        lineNumber = self.lexer.peek_token().lineNumber
        self.lexer.match(Keyword(0, "length"))
        self.lexer.match(Operator(0, "("))
        l = self.parse_expr()
        self.lexer.match(Operator(0,")"))
        return list_len(lineNumber, l)
    
    def parse_pop(self):
        self.lexer.match(Keyword(0, "pop"))
        self.lexer.match(Operator(0, "("))
        l=self.lexer.peek_token()
        if not isinstance(l, Identifier):
            ParseError(self, f"Expected an identifier", l.lineNumber)
        self.lexer.advance()
        self.lexer.match(Operator(0,")"))
        self.lexer.match(Operator(0,";"))
        var = Variable(l.lineNumber, l.val, generate_id())
        return list_pop(l.lineNumber, var)
    
    def parse_insert(self):
        lineNumber = self.lexer.peek_token().lineNumber
        self.lexer.match(Keyword(0, "insert"))
        self.lexer.match(Operator(0, "("))
        index=self.parse_expr()
        self.lexer.match(Operator(0,","))
        ele=self.parse_expr()
        self.lexer.match(Operator(0,","))
        l=self.lexer.peek_token()
        if not isinstance(l, Identifier):
            ParseError(self, f"Expected an identifier", l.lineNumber)
        self.lexer.advance()
        var = Variable(l.lineNumber, l.val, generate_id())
        self.lexer.match(Operator(0,")"))
        self.lexer.match(Operator(0,";"))
        return list_insert(lineNumber, index, ele, var)
    
    def parse_expr_stmt(self):
        t = self.parse_expr()
        self.lexer.match(Operator(0, ';'))
        return t
    
    def parse_atom(self):
        match self.lexer.peek_token():
            case Identifier(lineNumber, name):
                i = self.lexer.peek_token()
                self.lexer.advance()
                params = []
                if(self.lexer.peek_token().val == "("):
                    self.lexer.advance()
                    while(self.lexer.peek_token().val != ")"):
                        iden = self.parse_expr()
                        params.append(iden)

                        if self.lexer.peek_token().val == ',':
                            self.lexer.advance()

                    self.lexer.match(Operator(0,")"))
                    func = Variable(i.lineNumber, i.val, generate_id())
                    return FunCall(lineNumber, func, params)
                else:
                    return Variable(lineNumber, name, generate_id())
                
            case Keyword(lineNumber, "slice"):
                self.lexer.advance()
                val = self.parse_expr()
                start = self.parse_expr()
                self.lexer.match(Operator(0,":"))
                end = self.parse_expr()
                return Slice(lineNumber, val, start, end)
                
            case Keyword(lineNumber,"index"):
                self.lexer.advance()
                val = self.parse_expr()
                start = self.parse_expr()
                return Slice(lineNumber, val,start,nil())
            
            case Integer(lineNumber, value):
                self.lexer.advance()
                return Int(value)
            case Boolean(lineNumber, value):
                self.lexer.advance()
                return Bool(value)
            case String(lineNumber, value):
                self.lexer.advance()
                return Str(value)
            case Flt(lineNumber, value):
                self.lexer.advance()
                return Float(value)
            case Operator(lineNumber, '('):
                self.lexer.advance()
                l = self.parse_expr()
                self.lexer.match(Operator(0, ')'))
                return l
            case Operator(lineNumber, '['):
                self.lexer.advance()
                lst = zList(None, [])
                # Collecting expressions until we hit a ']'
                while (self.lexer.peek_token().val != ']'):
                    exp = self.parse_expr()
                    lst.elements.append(exp)
                    if (self.lexer.peek_token().val == ','):
                        self.lexer.advance()
                    elif(self.lexer.peek_token().val != ']'):
                        ParseError(self, f"Expected a \']\' or \',\'", self.lexer.peek_token().lineNumber)
                self.lexer.advance()
                return lst
            case other:
                ParseError(self, "Expected an Expression!", other.lineNumber)
    
    def parse_unary(self):
        op = self.lexer.peek_token()
        if(op.val in ["~","-"]) :
            self.lexer.advance()
            right = self.parse_unary()
            return UnOp(op.lineNumber, op.val,right)
        elif (op.val == "length"):
            return self.parse_len()
        return self.parse_atom()
    
    def parse_power(self):
        left = self.parse_unary()
        op = self.lexer.peek_token()
        if(op.val == "^"):
            self.lexer.advance()
            right = self.parse_power()
            return BinOp(op.lineNumber, op.val,left, right)
        return left
    
    def parse_mult(self):
        left = self.parse_power()
        while True:
            match self.lexer.peek_token():
                case Operator(lineNumber, op) if op in "*/%" or op == "//":
                    self.lexer.advance()
                    m = self.parse_power()
                    left = BinOp(lineNumber, op, left, m)
                case _:
                    break
        return left
    
    def parse_add(self):
        left = self.parse_mult()
        while True:
            match self.lexer.peek_token():
                case Operator(lineNumber, op) if op in ["+","-"]:
                    self.lexer.advance()
                    m = self.parse_mult()
                    left = BinOp(lineNumber, op, left, m)
                case _:
                    break
        return left

    def parse_shift(self):
        left = self.parse_add()
        while True:
            match self.lexer.peek_token():
                case Operator(lineNumber, op) if op in ["<<",">>"]:
                    self.lexer.advance()
                    m = self.parse_add()
                    left = BinOp(lineNumber, op, left, m)
                case _:
                    break
        return left
    
    def parse_comparision(self):
        left = self.parse_shift()
        while(isinstance(self.lexer.peek_token(), Operator) and self.lexer.peek_token().val in ["<",">",">=","<="]):
            op = self.lexer.peek_token()
            self.lexer.advance()
            right = self.parse_shift()
            left =  BinOp(op.lineNumber, op.val, left, right)
        return left
    
    def parse_equality(self):
        left = self.parse_comparision()
        while(self.lexer.peek_token().val in ["!=","=="]) :
            t = self.lexer.peek_token()
            self.lexer.advance()
            right = self.parse_comparision()
            left = BinOp(t.lineNumber, t.val,left,right)
        return left
    
    def parse_logic_and(self) :
        left = self.parse_equality()
        while(self.lexer.peek_token().val == "&&"):
            op = self.lexer.peek_token()
            self.lexer.advance()
            right = self.parse_equality()
            left = BinOp(op.lineNumber, op.val,left,right)
        return left
    
    def parse_logic_or(self) :
        left = self.parse_logic_and()
        while(self.lexer.peek_token().val == "||" ) :
            op = self.lexer.peek_token()
            self.lexer.advance()
            right = self.parse_logic_and()
            left = BinOp(op.lineNumber, op.val,left,right)
        return left
    
    def parse_assign(self):
        l = self.parse_logic_or()
        a = self.lexer.peek_token()
        if (a.val == "=") :
            op = self.lexer.peek_token()
            self.lexer.advance()
            t = self.parse_assign()
            return BinOp(op.lineNumber, op.val,l,t)
        return l
    
    def parse_expr(self):
        return self.parse_assign()
    
    def parse_statement(self):
        
        match self.lexer.peek_token():
            case Keyword(lineNumber, "if"):
                return self.parse_if()
            case Keyword(lineNumber, "while"):
                return self.parse_while()
            case Keyword(lineNumber, "zout"):
                return self.parse_print()
            case Keyword(lineNumber, "for"):
                return self.parse_for()
            case Keyword(lineNumber, "append"):
                return self.parse_append()
            case Keyword(lineNumber, "remove"):
                return self.parse_remove()
            case Keyword(lineNumber, "pop"):
                return self.parse_pop()
            case Keyword(lineNumber, "insert"):
                return self.parse_insert()
            case Operator(lineNumber,"{") :
                return self.parse_block()
            case _:
                return self.parse_expr_stmt()
    
    def set_list_type(self, dtypes, i, lst):
        '''
        Function to set the dtype of the zlist generated by parse_expr
        '''
        if (i > len(dtypes)):
            print("1,2,3")
            raise Exception()
        lst.dtype = dtypes[i]
        for j in range(len(lst.elements)):
            if (isinstance(lst.elements[j], zList)):
                self.set_list_type(dtypes, i+1, lst.elements[j])
            elif (dtypes[i] == zList):
                print("1,2,3")
                raise Exception()
    
    def empty_list_type(self, dtypes, i):
        '''
        Function to initialize the empty zlist
        '''
        if (dtypes[i] != zList):
            lst = zList(dtypes[i], [])
        else:
            lst = zList(dtypes[i], self.empty_list_type(dtypes, i+1))
        return lst
    
    def parse_fundec(self):
        lineNumber = self.lexer.peek_token().lineNumber

        self.lexer.match(Keyword(0,"func"))

        # Checking the return type of the function
        rt = self.lexer.peek_token()
        if self.lexer.peek_token().val not in dtypes:
            ParseError(self, f"Expected a data type but given {rt.val}", rt.lineNumber)
        
        # Assigning the return type of the function
        r = self.lexer.peek_token()
        r_type = dtypes_dict[r.val]
        self.lexer.advance()
        
        # Generating a Variable for the function
        f = self.lexer.peek_token()
        func = Variable(f.lineNumber, f.val, generate_id())
        self.lexer.advance()

        # Checking for the "("
        self.lexer.match(Operator(0,"("))

        # Obtaining all the parameters and the parameter types
        param_types = []
        params = []
        while (self.lexer.peek_token().val != ")") :
            dt = self.lexer.peek_token()    # The data type of the parameter
            
            # Invalid Data Type for the parameter
            if dt.val not in dtypes:
                ParseError(self, f"Expected a data type but given {dt.val}", dt.lineNumber)

            # Appending the data type to the params_type list
            param_types.append(dtypes_dict[dt.val])
            self.lexer.advance()

            # Obtaining the parameter name and appending to the params list
            iden = self.lexer.peek_token()
            self.lexer.advance()
            params.append(Variable(iden.lineNumber, iden.val, generate_id()))

            # Checking for the "," if there are more parameters
            if self.lexer.peek_token().val == ',':
                self.lexer.advance()

        self.lexer.match(Operator(0,")"))

        func_block = nil()
        if self.lexer.peek_token().val == ";" :
            self.lexer.advance()
        else :
            func_block = self.parse_block()

        return DeclareFun(lineNumber, func , r_type, param_types, params, func_block)
    
    def parse_vardec(self):
        isConst=None # Variable indicating the constness of the variable
        
        # The l value
        l=self.lexer.peek_token()

        # In case the variable is declared as const
        if(l.val == "const"):
            self.lexer.match(l)
            isConst=True
        else:
            isConst=False

        match self.lexer.peek_token():
            case Keyword(lineNumber, "int"):
                self.lexer.match(Keyword(0, "int"))
                
                # Getting the identifier
                iden = self.lexer.peek_token()

                # Checking if the identifier is a keyword
                if(iden.val in keywords):
                    ParseError(self, "Cannot use Keywords as Identifiers", lineNumber)
                # Checking if the identifier is a data type
                elif iden.val in dtypes or iden.val in ["true","false"]:
                    ParseError(self, "Expected an Identifier", lineNumber)
                self.lexer.match(iden)

                # Creating a varibale object
                var = Variable(iden.lineNumber, iden.val, generate_id())

                # Checking if the variable is declared without an initial value
                if(self.lexer.peek_token().val != "="):
                    self.lexer.match(Operator(0, ";"))
                    return Declare(lineNumber, var, nil(), Int, isConst)
                
                # Getting the initial value of the variable
                self.lexer.match(Operator(0, "="))
                ans=self.parse_expr_stmt()

                return Declare(lineNumber, var ,ans, Int, isConst)
            
            case Keyword(lineNumber, "float"):
                self.lexer.match(Keyword(0, "float"))
                
                # Getting the identifier
                iden = self.lexer.peek_token()

                # Checking if the identifier is a keyword
                if(iden.val in keywords):
                    ParseError(self, "Cannot use Keywords as Identifiers", lineNumber)
                # Checking if the identifier is a data type
                elif iden.val in dtypes or iden.val in ["true","false"]:
                    ParseError(self, "Expected an Identifier", lineNumber)
                self.lexer.match(iden)

                # Creating a varibale object
                var = Variable(iden.lineNumber, iden.val, generate_id())

                # Checking if the variable is declared without an initial value
                if(self.lexer.peek_token().val != "="):
                    self.lexer.match(Operator(0, ";"))
                    return Declare(lineNumber, var, nil(), Float, isConst)
                self.lexer.match(Operator(0, "="))

                # Getting the initial value of the variable
                ans=self.parse_expr_stmt()

                return Declare(lineNumber, var, ans, Float, isConst)
            
            case Keyword(lineNumber, "string"):
                self.lexer.match(Keyword(0, "string"))
                 # Getting the identifier
                iden = self.lexer.peek_token()

                # Checking if the identifier is a keyword
                if(iden.val in keywords):
                    ParseError(self, "Cannot use Keywords as Identifiers", lineNumber)
                # Checking if the identifier is a data type
                elif iden.val in dtypes or iden.val in ["true","false"]:
                    ParseError(self, "Expected an Identifier", lineNumber)
                self.lexer.match(iden)

                # Creating a varibale object
                var = Variable(iden.lineNumber, iden.val, generate_id())

                # Checking if the variable is declared without an initial value
                if(self.lexer.peek_token().val != "="):
                    self.lexer.match(Operator(0, ";"))
                    return Declare(lineNumber, var, nil(), Str, isConst)
                self.lexer.match(Operator(0, "="))

                # Getting the initial value of the variable
                ans=self.parse_expr_stmt()

                return Declare(lineNumber, var, ans, Str, isConst)
            
            case Keyword(lineNumber, "boolean"):
                self.lexer.match(Keyword(0, "boolean"))
                 # Getting the identifier
                iden = self.lexer.peek_token()

                # Checking if the identifier is a keyword
                if(iden.val in keywords):
                    ParseError(self, "Cannot use Keywords as Identifiers", lineNumber)
                # Checking if the identifier is a data type
                elif iden.val in dtypes or iden.val in ["true","false"]:
                    ParseError(self, "Expected an Identifier", lineNumber)
                self.lexer.match(iden)

                # Creating a varibale object
                var = Variable(iden.lineNumber, iden.val, generate_id())

                # Checking if the variable is declared without an initial value
                if(self.lexer.peek_token().val != "="):
                    self.lexer.match(Operator(0, ";"))
                    return Declare(lineNumber, var, nil(), Bool, isConst)
                self.lexer.match(Operator(0, "="))

                # Getting the initial value of the variable
                ans=self.parse_expr_stmt()

                return Declare(lineNumber, var, ans, Bool, isConst)
            
            case Keyword(lineNumber, "list"):
                # Disallowing constant lists
                if (isConst):
                    ParseError(self, "Cannot declare a list as const.", lineNumber)
                
                # Getting the data type of the list
                dtypes_ = [] # Holds the actual data type list declared i.e., [zlist zlist Int]
                self.lexer.advance()
                while(self.lexer.peek_token().val == "list"):
                    dtypes_.append(zList)
                    self.lexer.advance()
                dt = self.lexer.peek_token()
                if (dt.val not in dtypes_dict):
                    ParseError(self, "Expected data type.", dt.lineNumber)
                dtypes_.append(dtypes_dict[dt.val])
                self.lexer.advance()
                
                iden = self.lexer.peek_token()
                
                # Verifying the identifier
                if (not isinstance(iden, Identifier)):
                    ParseError(self, "Expected Identifier.", iden.lineNumber)
                self.lexer.advance()

                # Creating the variable object
                var = Variable(iden.lineNumber, iden.val, generate_id())

                lst = nil()
                if (self.lexer.peek_token().val == "="):
                    self.lexer.advance()

                    # Attaining the list from the initializer list
                    lst = self.parse_expr()
                    try:
                        # Setting the list types as well as ensuring the list dimensions match
                        self.set_list_type(dtypes_, 0, lst)
                    except:
                        # Raising the Dimension error
                        ParseError(self, f"Dimensions of the given list and initializer list do not match", self.lexer.peek_token().lineNumber)
                else:
                    # Generating empty list
                    lst = self.empty_list_type(dtypes_, 0)
                self.lexer.match(Operator(0, ";"))
                return Declare(lineNumber, var, lst, zList, False)
            
    def parse_declare(self):
        if self.lexer.peek_token().val == "func" :
            return self.parse_fundec()
        elif(self.lexer.peek_token().val not in dtypes):
            return self.parse_statement()
        else:
            return self.parse_vardec()
    
    def parse_program(self):
        seqs=[]
        while(self.lexer.peek_token() != EOF()) :
            # Using try except for catching the ParseException as well as TokenException
            try:
                seqs.append(self.parse_declare())
            except (ParseException, TokenException):
                global isParseError
                isParseError = True
        return Seq(seqs)

def parse(string):
    '''
    Return a Parsed AST as well as the isParseError flag corresponding to parsing
    '''
    # Reinitializing the isParseError to False
    global isParseError 
    isParseError = False

    # Returning the obtained AST as well as the flag isParseError
    programAST = Parser.parse_program (
        Parser(Lexer.from_stream(Stream.from_string(string)))
    )

    # Reraising the ParseException if isParseError is True
    if isParseError:
        raise ParseException
    
    return programAST

def test_parse():
    # print(parse("list int a = [1,2,3]; append(2,a); remove(2,a); insert(0,100,a); a[0:2];")) 
    # print(parse("append(2,a)"))
    # print(parse("func int add(int a,int b) { a+b;} add(2, 3);"))
    pp = pprint.PrettyPrinter(indent=4)
    p = parse("int a = 8 << 1;")
    pp.pprint(p)
    k = evaluate(p)
    print(k)

if __name__ == "__main__" :
    test_parse()
