from fractions import Fraction
from dataclasses import dataclass
from typing import Optional, NewType
from sim import *
from lexer import *
class IdentifierError(Exception):
    pass
@dataclass
class Parser:
    lexer: Lexer
    def from_lexer(lexer):
        return Parser(lexer)
    def parse_if(self):
        self.lexer.match(Keyword("if"))
        self.lexer.match(Operator("("))
        c = self.parse_expr()
        self.lexer.match(Operator(")"))
        self.lexer.match(Operator("{"))
        ifseq=[]
        while(self.lexer.peek_token() != Operator("}")) :
            t = self.parse_statement()
            ifseq.append(t)
        self.lexer.match(Operator("}"))
        if(self.lexer.peek_token() != Keyword("else")):
            return If(c, Seq(ifseq), None)
        self.lexer.match(Keyword("else"))
        self.lexer.match(Operator("{"))
        elseq=[]
        while(self.lexer.peek_token() != Operator("}")) :
            t = self.parse_statement()
            elseq.append(t)
        self.lexer.match(Operator("}"))
        return If(c,Seq(ifseq), Seq(elseq))
    def parse_while(self):
        self.lexer.match(Keyword("while"))
        self.lexer.match(Operator("("))
        c = self.parse_expr()
        self.lexer.match(Operator(")"))
        self.lexer.match(Operator("{"))
        wseq=[]
        while(self.lexer.peek_token() != Operator("}")) :
            t = self.parse_statement()
            wseq.append(t)
        self.lexer.match(Operator("}"))
        return While(c, Seq(wseq))
    def parse_print(self):
        self.lexer.match(Keyword("zout"))
        self.lexer.match(Operator("("))
        pseq=[]
        pseq.append(self.parse_expr())
        while(self.lexer.peek_token() != Operator(")")):
            self.lexer.match(Operator(","))
            t=self.parse_expr()
            pseq.append(t)
        self.lexer.match(Operator(")"))
        self.lexer.match(Operator(";"))
        return PRINT(pseq)
    def parse_expr_stmt(self):
        t=self.parse_expr()
        self.lexer.match(Operator(';'))
        return t
    def parse_atom(self):
        match self.lexer.peek_token():
            case Identifier(name):
                self.lexer.advance()
                return Variable(name)
            case Integer(value):
                self.lexer.advance()
                return Int(value)
            case Bool(value):
                self.lexer.advance()
                return Bool(value)
            case String(value):
                self.lexer.advance()
                return Str(value)
            case Flt(value):
                self.lexer.advance()
                return Float(value)
            case Operator('('):
                self.lexer.advance()
                l = self.parser_expr()
                self.lexer.match(Operator(')'))
                self.lexer.advance()
            case _:
                raise IdentifierError()
    def parse_unary(self):
        op = self.lexer.peek_token()
        if(op.val in ["~","-"]) :
            self.lexer.advance()
            right = self.parse_unary()
            return UnOp(right,op.val)
        return self.parse_atom()
    def parse_mult(self):
        left = self.parse_unary()
        while True:
            match self.lexer.peek_token():
                case Operator(op) if op in "*/":
                    self.lexer.advance()
                    m = self.parse_unary()
                    left = BinOp(op, left, m)
                case _:
                    break
        return left
    
    def parse_add(self):
        left = self.parse_mult()
        while True:
            match self.lexer.peek_token():
                case Operator(op) if op in ["+","-"]:
                    self.lexer.advance()
                    m = self.parse_mult()
                    left = BinOp(op, left, m)
                case _:
                    break
        return left
    def parse_comparision(self):
        left = self.parse_add()
        while(isinstance(self.lexer.peek_token(), Operator) and self.lexer.peek_token().val in ["<",">",">=","<="]):
            op = self.lexer.peek_token().val
            self.lexer.advance()
            right = self.parse_add()
            left =  BinOp(op, left, right)
        return left
    def parse_equality(self):
        left = self.parse_comparision()
        while(self.lexer.peek_token() in [Operator("!="),Operator("==")]) :
            t = self.lexer.peek_token()
            self.lexer.advance()
            right = self.parse_comparision()
            left = BinOp(t.val,left,right)
        return left
    def parse_logic_and(self) :
        left = self.parse_equality()
        while(self.lexer.peek_token() == Operator("&&")):
            self.lexer.advance()
            right = self.parse_equality()
            left = BinOp("&&",left,right)
        return left
    def parse_logic_or(self) :
        left = self.parse_logic_and()
        while(self.lexer.peek_token() == Operator("||") ) :
            self.lexer.advance()
            right = self.parse_logic_and()
            left = BinOp('||',left,right)
        return left
    def parse_assign(self):
        l = self.parse_logic_or()
        a = self.lexer.peek_token()
        if (a == Operator("=")) :
            self.lexer.advance()
            t = self.parse_assign()
            return BinOp("=",l,t)
        return l
    def parse_expr(self):
        return self.parse_assign()
    def parse_statement(self):
        match self.lexer.peek_token():
            case Keyword("if"):
                return self.parse_if()
            case Keyword("while"):
                return self.parse_while()
            case Keyword("zout"):
                return self.parse_print()
            case _:
                return self.parse_expr_stmt()
    def parse_vardec(self):
        found=None
        l=self.lexer.peek_token()
        if(l == Keyword("const")):
            self.lexer.match(l)
            found=True
        else:
            found=False
        match self.lexer.peek_token():
            case Keyword("int"):
                self.lexer.match(Keyword("int"))
                b=self.lexer.peek_token()
                if(b.val in keywords or b.val in dtypes or b.val in ["true","false"]):
                    raise IdentifierError()
                self.lexer.match(b)
                if(self.lexer.peek_token()!=Operator("=")):
                    self.lexer.match(Operator(";"))
                    return Declare(Variable(b.val),nil(), nil(), nil())
                self.lexer.match(Operator("="))
                ans=self.parse_expr_stmt()
                return Declare(Variable(b.val),ans, Int, found)
            case Keyword("float"):
                self.lexer.match(Keyword("float"))
                b=self.lexer.peek_token()
                if(b.val in keywords or b.val in dtypes or b.val in ["true","false"]):
                    raise IdentifierError()
                self.lexer.match(b)
                if(self.lexer.peek_token()!=Operator("=")):
                    self.lexer.match(Operator(";"))
                    return Declare(Variable(b.val),nil(), nil(), nil())
                self.lexer.match(Operator("="))
                ans=self.parse_expr_stmt()
                return Declare(Variable(b.val),ans, Float, found)
            case Keyword("string"):
                self.lexer.match(Keyword("string"))
                b=self.lexer.peek_token()
                if(b.val in keywords or b.val in dtypes or b.val in ["true","false"]):
                    raise IdentifierError()
                self.lexer.match(b)
                if(self.lexer.peek_token()!=Operator("=")):
                    self.lexer.match(Operator(";"))
                    return Declare(Variable(b.val),nil(), nil(), nil())
                self.lexer.match(Operator("="))
                ans=self.parse_expr_stmt()
                return Declare(Variable(b.val),ans, Str , found)
            case Keyword("boolean"):
                self.lexer.match(Keyword("boolean"))
                b=self.lexer.peek_token()
                if(b.val in keywords or b.val in dtypes or b.val in ["true","false"]):
                    raise IdentifierError()
                self.lexer.match(b)
                if(self.lexer.peek_token()!=Operator("=")):
                    self.lexer.match(Operator(";"))
                    return Declare(Variable(b.val),nil(), nil(), nil())
                self.lexer.match(Operator("="))
                ans=self.parse_expr_stmt()
                return Declare(Variable(b.val),ans, Bool , found)
            
    def parse_declare(self):
        if(self.lexer.peek_token().val not in dtypes):
            return self.parse_statement()
        else:
            return self.parse_vardec()
    def parse_program(self):
        seqs=[]
        while(self.lexer.peek_token() != EOF()) :
            seqs.append(self.parse_declare())
        return Seq(seqs)
def parse(string):
    return Parser.parse_program (
        Parser.from_lexer(Lexer.from_stream(Stream.from_string(string)))
    )


