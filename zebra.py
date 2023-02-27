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
    try: 
        stream = None
        with open(path, 'r') as file:
            stream = '\n'.join(file.readlines())
        execute(stream)

    except:
        InvalidProgram(Exception(f"Specified file at {path} does not exist!"));

def execute(stream: str):
    programAST = parse(stream)
    typecheck(programAST)
    if (not isError):
        try:
            output = evaluate(programAST)
            return output
        except Exception as e:
            print(repr(e))
            return nil()
    return nil()

def executeInteractive(stream:str, typecheckerScopes: TypecheckerScopes, scopes: Scopes):
    programAST = parse(stream)
    typecheck(programAST, typecheckerScopes)
    if (not isError):
        try: 
            output = evaluate(programAST, scopes)
            return output
        except Exception as e:
            print(repr(e))
            return nil()
    return nil()

def interactiveShell():
    '''
    Run the lanuage in interactive shell form
    '''
    # Creating Scopes
    scopes = Scopes()

    # Creating scopes for typechecking
    typecheckerScopes = TypecheckerScopes()

    while True:
        print(">>", end = " ")
        lines = ""
        while(True):
            line = input().strip()
            
            if (line.endswith('\\')):
                line = line[:-1]
                lines += line 
            else:
                lines += line 
                break
        
        # Way to exit the shell
        if (lines.strip() == "exit") :
            print("Goodbye")
            break
        
        output = executeInteractive(lines, typecheckerScopes, scopes)
        
        # Printing output only if it returns something
        if (output != nil()):
            print(output)
        print()

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
