from fractions import Fraction
from dataclasses import dataclass
from typing import Optional, NewType
from sim import *
from lexer import *
from error import ParseError, ParseException, TokenException

# Global value denoting if the Parse Error occured
isParseError = False

# Data Types dictionary
dtypes_dict = {
    "int" : Int, 
    "float": Float, 
    "string": Str, 
    "boolean": Bool
}
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
        return Seq(block_seq)
    

    def parse_if(self):
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
        
        return If(c,if_block, else_block)

    def parse_for(self):
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
            for_block.lines.append(order)
        return For(initial,condition,for_block)
        
    
    def parse_while(self):
        self.lexer.match(Keyword(0, "while"))
        self.lexer.match(Operator(0, "("))
        c = self.parse_expr()
        self.lexer.match(Operator(0, ")"))
        w_block = self.parse_block()
        return While(c, w_block)
    
    def parse_print(self):
        self.lexer.match(Keyword(0, "zout"))
        self.lexer.match(Operator(0, "("))
        pseq=[]
        pseq.append(self.parse_expr())
        while(self.lexer.peek_token().val != ")"):
            self.lexer.match(Operator(0, ","))
            t=self.parse_expr()
            pseq.append(t)
        self.lexer.match(Operator(0, ")"))
        self.lexer.match(Operator(0, ";"))
        return PRINT(pseq)

    def parse_append(self):
        self.lexer.match(Keyword(0, "append"))
        self.lexer.match(Operator(0,"("))
        ele=self.parse_expr()
        self.lexer.match(Operator(0,","))
        l=self.lexer.peek_token()
        if not isinstance(l, Identifier):
            ParseError(f"Expected an identifier", l.lineNumber)
        self.lexer.advance()
        self.lexer.match(Operator(0,")"))
        return list_append(ele, l)
    
    def parse_remove(self):
        self.lexer.match(Keyword(0, "remove"))
        self.lexer.match(Operator(0, "("))
        index=self.parse_expr()
        self.lexer.match(Operator(0,","))
        l=self.lexer.peek_token()
        if not isinstance(l, Identifier):
            ParseError(f"Expected an identifier", l.lineNumber)
        self.lexer.advance()
        self.lexer.match(Operator(0,")"))
        return list_remove(index, l)
    
    def parse_len(self):
        self.lexer.match(Keyword(0, "length"))
        self.lexer.match(Operator(0, "("))
        l=self.lexer.peek_token()
        if not isinstance(l, Identifier):
            ParseError(f"Expected an identifier", l.lineNumber)
        self.lexer.advance()
        self.lexer.match(Operator(0,")"))
        return list_len(l)
    
    def parse_insert(self):
        self.lexer.match(Keyword(0, "insert"))
        self.lexer.match(Operator(0, "("))
        index=self.parse_expr()
        self.lexer.match(Operator(0,","))
        ele=self.parse_expr()
        self.lexer.match(Operator(0,","))
        l=self.lexer.peek_token()
        if not isinstance(l, Identifier):
            ParseError(f"Expected an identifier", l.lineNumber)
        self.lexer.advance()
        self.lexer.match(Operator(0,")"))
        return list_insert(index, ele, l)
    
    def parse_expr_stmt(self):
        t = self.parse_expr()
        self.lexer.match(Operator(0, ';'))
        return t
    
    def parse_atom(self):
        match self.lexer.peek_token():
            case Identifier(lineNumber, name):
                self.lexer.advance()
                return Variable(name)
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
                while (True):
                    exp = self.parse_expr()
                    lst.elements.append(exp)
                    if (self.lexer.peek_token().val == ','):
                        self.lexer.advance()
                    elif (self.lexer.peek_token().val == ']'):
                        self.lexer.advance()
                        break
                    else:
                        ParseError(self, f"Expected a \']\' and \',\'", self.lexer.peek_token().lineNumber)
                return lst
            case other:
                ParseError(self, "Expected an Expression!", other.lineNumber)
    
    def parse_unary(self):
        op = self.lexer.peek_token()
        if(op.val in ["~","-"]) :
            self.lexer.advance()
            right = self.parse_unary()
            return UnOp(right,op)
        return self.parse_atom()
    
    def parse_mult(self):
        left = self.parse_unary()
        while True:
            match self.lexer.peek_token():
                case Operator(lineNumber, op) if op in "*/":
                    self.lexer.advance()
                    m = self.parse_unary()
                    left = BinOp(Operator(lineNumber, op), left, m)
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
                    left = BinOp(Operator(lineNumber, op), left, m)
                case _:
                    break
        return left
    
    def parse_comparision(self):
        left = self.parse_add()
        while(isinstance(self.lexer.peek_token(), Operator) and self.lexer.peek_token().val in ["<",">",">=","<="]):
            op = self.lexer.peek_token()
            self.lexer.advance()
            right = self.parse_add()
            left =  BinOp(op, left, right)
        return left
    
    def parse_equality(self):
        left = self.parse_comparision()
        while(self.lexer.peek_token().val in ["!=","=="]) :
            t = self.lexer.peek_token()
            self.lexer.advance()
            right = self.parse_comparision()
            left = BinOp(t,left,right)
        return left
    
    def parse_logic_and(self) :
        left = self.parse_equality()
        while(self.lexer.peek_token().val == "&&"):
            op = self.lexer.peek_token()
            self.lexer.advance()
            right = self.parse_equality()
            left = BinOp(op,left,right)
        return left
    
    def parse_logic_or(self) :
        left = self.parse_logic_and()
        while(self.lexer.peek_token().val == "||" ) :
            op = self.lexer.peek_token()
            self.lexer.advance()
            right = self.parse_logic_and()
            left = BinOp(op,left,right)
        return left
    
    def parse_assign(self):
        l = self.parse_logic_or()
        a = self.lexer.peek_token()
        if (a.val == "=") :
            op = self.lexer.peek_token()
            self.lexer.advance()
            t = self.parse_assign()
            return BinOp(op,l,t)
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
            case Keyword(lineNumber, "length"):
                return self.parse_len()
            case Keyword(lineNumber, "insert"):
                return self.parse_insert()
            case Keyword(lineNumber,"{") :
                return self.parse_block()
            case _:
                return self.parse_expr_stmt()
    
    def set_list_type(self, dtypes, i, lst):
        '''
        Function to set the dtype of the zlist generated by parse_expr
        '''
        if (i > len(dtypes)):
            raise Exception()
        lst.dtype = dtypes[i]
        for j in range(len(lst.elements)):
            if (isinstance(lst.elements[j], zList)):
                self.set_list_type(dtypes, i+1, lst.elements[j])
            elif (dtypes[i] == zList):
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
        self.lexer.match(Keyword(0,"func"))

        if self.lexer.peek_token().val not in dtypes:
            ParseError(self, f"Expected a data type but given {self.lexer.peek_token().val}", lineNumber)
        
        r = self.lexer.peek_token()
        r_type = dmap[r.val]
        self.lexer.advance()

        func = self.lexer.peek_token()
        self.lexer.advance()
        self.lexer.match(Operator(0,"("))

        param_types = []
        params = []
        while (self.lexer.peek_token() != Operator(0,")")) :
            dt = self.lexer.peek_token()
            if self.lexer.peek_token().val not in dtypes:
                ParseError(self, f"Expected a data type but given {self.lexer.peek_token().val}", lineNumber)

            param_types.append(dmap[dt.val])
            self.lexer.advance()

            iden = self.lexer.peek_token()
            self.lexer.advance()
            params.append(iden)

            if self.lexer.peek_token().val == ',':
                self.lexer.advance()

        self.lexer.match(Operator(0,")"))

        func_block = nil()
        if self.lexer.peek_token().val == ";" :
            self.lexer.advance()
        else :
            func_block = self.parse_block()
        

        return DeclareFun(func , param_types,params,func_block)
        
    
    def parse_vardec(self):
        
        found=None
        l=self.lexer.peek_token()
        if(l.val == "const"):
            self.lexer.match(l)
            found=True
        elif l.val == "list":
            dtypes = []
            self.lexer.advance()
            while(self.lexer.peek_token().val == "list"):
                dtypes.append(zList)
                self.lexer.advance()
            if (self.lexer.peek_token().val not in dtypes_dict):
                ParseError(self, "Expected data type.", self.lexer.peek_token().lineNumber)
            dtypes.append(dtypes_dict[self.lexer.peek_token().val])
            self.lexer.advance()
            if (not isinstance(self.lexer.peek_token(), Identifier)):
                ParseError(self, "Expected Identifier.", self.lexer.peek_token().lineNumber)
            var = self.lexer.peek_token()
            self.lexer.advance()
            lst = nil()
            if (self.lexer.peek_token().val == "="):
                self.lexer.advance()
                lst = self.parse_expr()
                try:
                    self.set_list_type(dtypes, 0, lst)
                except:
                    ParseError(self, f"Dimensions of the given list and initializer list do not match", self.lexer.peek_token().lineNumber)
            else:
                lst = self.empty_list_type(dtypes, 0)
            self.lexer.match(Operator(0, ";"))
            return Declare(var, lst, zList, False)

        else:
            found=False
        match self.lexer.peek_token():
            case Keyword(lineNumber, "int"):
                self.lexer.match(Keyword(0, "int"))
                b = self.lexer.peek_token()
                if(b.val in keywords or b.val in dtypes or b.val in ["true","false"]):
                    ParseError(self, "Expected a '=' or ';'", lineNumber)
                self.lexer.match(b)
                if(self.lexer.peek_token().val != "="):
                    self.lexer.match(Operator(0, ";"))
                    return Declare(b, nil(), Int, found)
                self.lexer.match(Operator(0, "="))
                ans=self.parse_expr_stmt()
                return Declare(b,ans, Int, found)
            case Keyword(lineNumber, "float"):
                self.lexer.match(Keyword(0, "float"))
                b=self.lexer.peek_token()
                if(b.val in keywords or b.val in dtypes or b.val in ["true","false"]):
                    ParseError(self, "Expected a '=' or ';'", lineNumber)
                self.lexer.match(b)
                if(self.lexer.peek_token().val != "="):
                    self.lexer.match(Operator(";"))
                    return Declare(b,nil(), Float, found)
                self.lexer.match(Operator(0, "="))
                ans=self.parse_expr_stmt()
                return Declare(b,ans, Float, found)
            case Keyword(lineNumber, "string"):
                self.lexer.match(Keyword(0, "string"))
                b=self.lexer.peek_token()
                if(b.val in keywords or b.val in dtypes or b.val in ["true","false"]):
                    ParseError(self, "Expected a '=' or ';'", lineNumber)
                self.lexer.match(b)
                if(self.lexer.peek_token().val != "="):
                    self.lexer.match(Operator(";"))
                    return Declare(b,nil(), Str, found)
                self.lexer.match(Operator(0,"="))
                ans=self.parse_expr_stmt()
                return Declare(b,ans, Str , found)
            case Keyword(lineNumber, "boolean"):
                self.lexer.match(Keyword(0, "boolean"))
                b=self.lexer.peek_token()
                if(b.val in keywords or b.val in dtypes or b.val in ["true","false"]):
                    ParseError(self, "Expected a '=' or ';'", lineNumber)
                self.lexer.match(b)
                if(self.lexer.peek_token().val !="="):
                    self.lexer.match(Operator(0, ";"))
                    return Declare(b,nil(), Bool, found)
                self.lexer.match(Operator(0, "="))
                ans=self.parse_expr_stmt()
                return Declare(b,ans, Bool , found)
            
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
    return Parser.parse_program (
        Parser.from_lexer(Lexer.from_stream(Stream.from_string(string)))
    ), isParseError

def test_parse():
    print(parse("list int a = [1,2,3]; append(2,a) remove(2,a) insert(0,100,a) length(a)")) 
    # print(parse("append(2,a)"))

if __name__ == "__main__" :
    test_parse()
