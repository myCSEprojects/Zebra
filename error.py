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
        print(f"\x1B[1;31m{self.type_}\x1B[0m(\x1B[96mline:\x1B[32m{self.lineNumber}\x1B[0m): {self.message_}")

class RuntimeException(Exception):
    pass

def RuntimeError(message_: str, lineNumber: int, type_: str="runtimeError"):
    ''''
    function for reporting runtime errors
    '''
    Error(type_, message_, lineNumber).report()
    raise RuntimeException() # to be caught in the excecute function

# Type checking exception to be caught in the typecheckAST function
class TypeCheckException(Exception):
    pass

# Function to raise Type Check errors
def typeCheckError(message_: str, lineNumber: int, type_: str="typeCheckError"):
    Error(message_, lineNumber, type_).report()

    # Raising the TypeCheckException to be caught in the typecheckAST function
    raise TypeCheckException()

class ParseException(Exception):
    '''
    Class for parse exception to be caught by parse_program
    '''
    pass

def ParseError(parser, message_: str, lineNumber: int, type_: str="ParseError"):
        '''
        Way to report Parse Error
        '''
        # Reporting the error
        Error(type_ , message_, lineNumber).report()

        # Synchronizing the lexer
        parser.lexer.synchronize()

        # Raising the parseException to be caught using parse program
        raise ParseException

class TokenException(Exception):
    '''
    Class for raising the TokenException to be caught by the parseProgram
    '''
    pass

def TokenError(lexer, message_: str, lineNumber: int, type_: str="TokenError"):
        '''
        Way to report Token Error
        '''
        # Reporting the error
        Error(type_ , message_, lineNumber).report()

        # Synchronizing the lexer
        lexer.synchronize()

        # Raising the parseException to be caught using parse program
        raise TokenException