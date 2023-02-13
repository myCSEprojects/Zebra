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
        print(self.lexer.peek_token())
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
                print(f"float {value}")
                self.lexer.advance()
                print(Float(value))
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


