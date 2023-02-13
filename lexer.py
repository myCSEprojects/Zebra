from fractions import Fraction
from dataclasses import dataclass
from typing import Optional, NewType

# A minimal example to illustrate typechecking.

class EndOfStream(Exception):
    pass

@dataclass
class Stream:
    source: str
    pos: int

    def from_string(s):
        return Stream(s, 0)

    def next_char(self):
        if self.pos >= len(self.source):
            raise EndOfStream()
        self.pos = self.pos + 1
        return self.source[self.pos - 1]

    def unget(self):
        assert self.pos > 0
        self.pos = self.pos - 1

    def pres(self):
        return self.source[self.pos]

# Define the token types.

@dataclass
class Integer:
    val: int

@dataclass
class Bool:
    val: bool

@dataclass
class Keyword:
    val: str

@dataclass
class Identifier:
    val: str
        
@dataclass
class Operator:
    val: str

@dataclass 
class String:
    val:str

@dataclass
class Flt:
    val:float

@dataclass 
class EOF:
    pass

Token = Integer | Bool | Keyword | Identifier | Operator | Flt

class EndOfTokens(Exception):
    pass

keywords = "if else while for zout".split()
dtypes = "int float string boolean const".split()
symbolic_operators = "+ - * / < > ! = ; { } ( ) , ~ % & | ~".split()
str_denote = ["'",'"']
whitespace = " \t\n"

def word_to_token(word):
    if (word in keywords) or (word in dtypes):
        return Keyword(word)
    if word == "true":
        return Bool(True)
    if word == "false":
        return Bool(False)
    return Identifier(word)

class TokenError(Exception):
    pass


@dataclass
class Lexer:
    stream: Stream
    save: Token = None

    def from_stream(s):
        return Lexer(s)

    def next_token(self) -> Token:
        try:
            next_chr =  self.stream.next_char()

            match next_chr:

                case c if c in symbolic_operators: 
                    s = str(c)
                    if(s == ">" or "<" or "!" or "=" or  "&" or "/" or "|"):
                        while True:
                            try:
                                c = self.stream.next_char()
                                if ((s=="!" or s=="<" or s==">") and c == "=") or (c==s and (s==">" or s=="<" or s=="=" or s=="&" or s=="|")):
                                    s = s + str(c) 
                                    return(Operator(s))
                                else:
                                    self.stream.unget()
                                    return (Operator(s))
                            
                            except EndOfStream:
                                return (Operator(s))

                    return Operator(s)         

                case c if c in str_denote:
                    s=""
                    while True:
                        try:
                            c = self.stream.next_char()
                            if c == next_chr:
                                return String(s)
                            else:
                                s = s+str(c)

                        except:
                            raise Exception("String not closed")                           

                case c if c.isdigit():
                    n = int(c)
                    d = "0."
                    is_decimal = True

                    while True:
                        try:
                            c = self.stream.next_char()
                            if c.isdigit():
                                n = n*10 + int(c)

                            elif c=='.':
                                try:
                                    while True:
                                        c = self.stream.next_char()
                                        if c.isdigit():
                                            d = d + str(c) 
                                        else:
                                            self.stream.unget()
                                            if (self.stream.pres() == '.'):
                                                raise Exception("Invalid literal found")
                                            
                                            return Flt((n+float(d)))

                                except:
                                    if d=="0.":
                                        raise Exception("Invalid literal found")
                                    return Flt((n+float(d)))

                                
                            else:
                                self.stream.unget()
                                return Integer(n)

                        except EndOfStream:
                            return Integer(n)

                case c if c.isalpha():
                    s = c
                    while True:
                        try:
                            c = self.stream.next_char()
                            if c.isalpha():
                                s = s + c
                            else:
                                self.stream.unget()
                                return word_to_token(s)
                        except EndOfStream:
                            return word_to_token(s)

                case c if c in whitespace:
                    return self.next_token()

                case _:
                    raise Exception("Invalid literal")
            
        except EndOfStream:
            return EOF()



    def peek_token(self) -> Token:
        if self.save is not None:
            return self.save
        self.save = self.next_token()
        return self.save

    def advance(self):
        assert self.save is not None
        self.save = None

    def match(self, expected):
        if self.peek_token() == expected:
            return self.advance()
        raise TokenError()

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self.next_token()
        except EndOfTokens:
            raise StopIteration

