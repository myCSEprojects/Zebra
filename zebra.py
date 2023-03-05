import sys
from parser import *
from typechecking import *
from sim import *
import readline

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
        InvalidProgram(Exception(f"Specified file at {path} does not exist!"));
    execute(stream)

def execute(stream: str):
    '''
    Execute a given string
    '''
    global isError
    # Parsing the given string
    programAST, isError = parse(stream)
    
    # Exiting in case of parsing errors
    if (isError):
        return nil()
    
    # Perform type checking for the produced ast
    typecheck(programAST)
    
    if (not isError):
        # Try to execute in case of no runtime errors
        try:
            output = evaluate(programAST)
            return output
        # Catching all runtime exceptions
        except Exception as e:
            return nil()
    return nil()

def executeInteractive(stream:str, typecheckerScopes: TypecheckerScopes, scopes: Scopes):
    global isError
    if (not isError):
        try: 
            programAST, isError = parse(stream)
            print(programAST)
            # Exiting if there were any errors during parsing
            if (isError):
                return
            typecheck(programAST, typecheckerScopes)
            output = evaluate(programAST, scopes)
            return output
        except Exception as e:
            # An uncaught expression for development purpose
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
    typecheckerScopes = TypecheckerScopes()

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
            output = executeInteractive(lines, typecheckerScopes, scopes)
            
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
