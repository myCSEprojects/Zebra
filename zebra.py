import sys
from parser import *
from typechecking import *
from sim import *
from error import RuntimeException
try:
    import readline
except:
    from pyreadline3 import Readline
    readline = Readline()

# Global error flag also takes care of exceptions
isError = False

# Function definitions
def executeFile(path: str):
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
    
    execute(stream, Scopes(), Scopes())

def execute(stream:str, typecheckerScopes: TypecheckerScopes, scopes: Scopes):
    global isError
    try: 
        programAST, isError = parse(stream) # any ParseError in the stream would be caught in the parse function and the error flag would be set
        # Exiting if there were any errors during parsing
        if (isError):
            return nil()
        # Performing typechecking
        isError = typecheckAST(programAST, typecheckerScopes) # any TypecheckError in the stream would be caught in the typecheckAST function and the error flag would be set
        # Exiting if there were any errors during typechecking
        if (isError):
            return nil()
        # Catching any runtime errors
        output = nil()
        try:
            output = evaluate(programAST, scopes)
        except RuntimeException as e:
            isError = True
        return output
    except Exception as e:
        # An uncaught expression for development purpose (Due to unhandled cases in the parser)
        raise e
    return nil()

def interactiveShell():
    '''
    Run the lanuage in interactive shell form
    '''

    global isError

    # Creating Scopes
    scopes = Scopes()

    # Creating scopes for typechecking
    typecheckerScopes = Scopes()

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
            output = execute(lines, typecheckerScopes, scopes)
            
            # Printing new line after each line
            print()

            isError = False
            
    except KeyboardInterrupt:
        print("GoodBye")

if __name__ == "__main__":
    
    args = sys.argv

    n = len(args)

    if (n > 2):
        # Error (Invalid arguments provided)
        print("Invalid Number of arguments")
        exit(-1)

    elif (n == 2):
        # Runninng the given script
        executeFile(args[1])
    else:
        # Running the interactive shell
        interactiveShell()
