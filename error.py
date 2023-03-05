from dataclasses import dataclass

@dataclass
class Error:
    '''
    Class for raising syntax, type, and resolve errors
    '''
    type_:str           # Denotes the type of the error(one of Type, Syntax, and Resolve)
    message_:str        # Custom message of the error
    lineNumber: int     # Line number obtained from the token

    def report(self):
        print(f"{self.type_}({self.lineNumber}):{self.message_}")

@dataclass
class RuntimeException:
    ''''
    Class for raising runtime exceptions
    '''
    type_:str
    message_:str
    lineNumber: int

    def raise_(self):
        print(f"{(self.type_ + ': ') if (self.type_) else ' '}{self.lineNumber}\n{self.message}")
        raise Exception()