from fractions import Fraction
from dataclasses import dataclass
from typing import Optional, NewType
from error import TokenError

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
class Token:
    lineNumber: int

@dataclass
class Integer(Token):
    val: int

@dataclass
class Keyword(Token):
    val: str

@dataclass
class Identifier(Token):
    val: str
        
@dataclass
class Operator(Token):
    val: str

@dataclass 
class String(Token):
    val:str

@dataclass
class Flt(Token):
    val:float

@dataclass
class Boolean(Token):
    val:bool

@dataclass 
class EOF:
    val = None

Integer | Boolean | Keyword | Identifier | Operator | Flt

class EndOfTokens(Exception):
    pass

keywords = "if else while for zout list append remove length insert func slice index".split()
dtypes = "int float string boolean const list".split()
symbolic_operators = "+ - * / < > ! = ; { } ( ) [ ] , ~ % & | ~ @ ^ :".split()
str_denote = ["'",'"']
whitespace = " \t\n"

def word_to_token(lineNumber, word):
    if (word in keywords) or (word in dtypes):
        return Keyword(lineNumber,word)
    if word == "true":
        return Boolean(lineNumber, True)
    if word == "false":
        return Boolean(False)
    return Identifier(lineNumber,word)

@dataclass
class Lexer:
    stream: Stream
    save: Token = None
    lineNumber = 0
    
    def synchronize(self):
        '''
        Synchronize this parser to a (next statement | EOF) in case of any errors
        '''
        while(self.peek_token() != EOF()):
            if (self.peek_token().val == ";"):
                self.advance()
                return
            self.advance()

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
                                    return(Operator(self.lineNumber,s))
                                else:
                                    self.stream.unget()
                                    return (Operator(self.lineNumber,s))
                            
                            except EndOfStream:
                                return (Operator(self.lineNumber,s))

                    return Operator(self.lineNumber,s)         

                case c if c in str_denote:
                    s=""
                    while True:
                        try:
                            c = self.stream.next_char()
                            if c == next_chr:
                                return String(self.lineNumber,s)
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
                                            
                                            return Flt(self.lineNumber,(n+float(d)))

                                except:
                                    if d=="0.":
                                        raise Exception("Invalid literal found")
                                    return Flt(self.lineNumber,(n+float(d)))

                                
                            else:
                                self.stream.unget()
                                return Integer(self.lineNumber,n)

                        except EndOfStream:
                            return Integer(self.lineNumber,n)

                case c if c.isalpha():
                    s = c
                    while True:
                        try:
                            c = self.stream.next_char()
                            if c.isalpha():
                                s = s + c
                            else:
                                self.stream.unget()
                                return word_to_token(self.lineNumber, s)
                        except EndOfStream:
                            return word_to_token(self.lineNumber, s)

                case c if c in whitespace:
                    # increasing the line number in case of 
                    if (c == '\n'):
                        self.lineNumber += 1
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
        # Check for the token
        if self.peek_token().val == expected.val:
            return self.advance()
        
        # Report the corresponding token error and raise token exception
        TokenError(self, f"Expected a '{expected.val}'", self.lineNumber)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self.next_token()
        except EndOfTokens:
            raise StopIteration

