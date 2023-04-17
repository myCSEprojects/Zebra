import sys
from parser import *
from typechecking import *
from sim import *
import pprint
from error import *
from resolver import *
import time 
from sim_BC import VM, codegen
try:
    import readline
except:
    from pyreadline3 import Readline
    readline = Readline()

# Global error flag also takes care of exceptions
isError = False

# Function definitions
def executeFile(path: str, evaluation_time: bool = False, byte_code: bool = False):
    '''
    Executes the file at the given path
    '''
    # Try to obtain the stream of characters
    try: 
        stream = None
        with open(path, 'r') as file:
            stream = ''.join(file.readlines()).strip()
    # In case the given file location is invalid
    except:
        print(f"Specified file at {path} does not exist!")
        exit(-1)
    
    execute(stream, ResolverScopes(), Scopes(), Scopes(), evaluation_time, byte_code)

def execute(stream:str, resolverScopes: ResolverScopes, typecheckerScopes: Scopes, scopes: Scopes, evaluation_time: bool = False, byte_code: bool = False):
    global isError
    try: 
        programAST = parse(stream)

        pp = pprint.PrettyPrinter(indent=4)

        resolvedProgram = resolve(programAST, resolverScopes)

        typecheckAST(resolvedProgram, typecheckerScopes) # any TypecheckError in the stream would be caught in the typecheckAST function and the error flag would be set
            
        if not byte_code:

            if evaluation_time:
                start = time.time()
            
            # Evaluating using tree walk
            output = evaluate(resolvedProgram, scopes)
            
            if evaluation_time:
                end = time.time()
                print("Evaluation time: ", end - start)
            
            return output
        
        else:
            if evaluation_time:
                start = time.time()
            
            # Evaluating using bytecode
            vm = VM()
            bytecode = codegen(resolvedProgram)
            vm.load(bytecode)
            output = vm.execute()
            
            if evaluation_time:
                end = time.time()
                print("Evaluation time: ", end - start)      
    
    except (RuntimeException, TypeCheckException, ParseException, ResolveException, RecursionError) as e:
        isError = True
        return nil()
    
    except Exception as e:
        # An uncaught expression for development purpose (Due to unhandled cases in the parser)
        raise e

def interactiveShell(evaluation_time: bool = False, byte_code: bool = False):
    '''
    Run the lanuage in interactive shell form
    '''

    global isError

    # Creating Scopes
    scopes = Scopes()

    # Creating scopes for typechecking
    typecheckerScopes = Scopes()

    # Creating scopes for resolving
    resolverScopes = ResolverScopes()

    try:
        while True:
            
            # variable to get all the lines
            lines = ""
            
            # Initially get line as input
            line = input(">> ").strip()
            lines += line 

            # Take input until the no line is given if the line does not end with ";"
            if (not line.endswith(';')):
                while(line != ""):
                    line = input(".. ").strip()
                    if (line != ""):
                        lines += line
            
            # Way to exit the shell
            if (lines.strip() == "exit") :
                print("Goodbye")
                break
            
            # Executing the lines
            output = execute(lines, resolverScopes, typecheckerScopes, scopes, evaluation_time, byte_code)
            
            # Printing new line after each line
            print()

            isError = False
            
    except KeyboardInterrupt:
        print("GoodBye")

if __name__ == "__main__":
    
    import argparse
 
    parser = argparse.ArgumentParser(description ='Main zebra interpreter')
    
    parser.add_argument('filename', nargs='?')                                           # positional argument
    parser.add_argument('-et', '--evaluation_time', action="store_true")      # option that takes a value
    parser.add_argument('-bc', '--byte_code', action='store_true')
    args = parser.parse_args()
    
    if args.filename:
        executeFile(args.filename, args.evaluation_time, args.byte_code)
    else:
        interactiveShell(args.evaluation_time, args.byte_code)
