import sys
from parser import *
from typechecking import *
from sim import *

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

def executeInteractive(stream:str, typecheckerScopes: TypecheckerScopes, scopes: Scopes):
    programAST = parse(stream)
    print(programAST)
    typecheck(programAST, typecheckerScopes)
    return evaluate(programAST, scopes)

def interactiveShell():
    '''
    Run the lanuage in interactive shell form
    '''
    scopes = Scopes()
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

        if (lines.strip() == "exit") :
            print("Goodbye")
            break
        print(lines)
        output = executeInteractive(lines, typecheckerScopes, scopes)
        if (output != nil()):
            print()
            print(output)

def execute(stream: str):
    programAST = parse(stream)
    typecheck(programAST)
    return evaluate(programAST)

if __name__ == "__main__":
    
    args = sys.argv

    n = len(args)

    if (n > 2):
        # Error (Invalid arguments provided)
        print("Invalid Number of arguments")
        exit(-1)
    elif (n == 2):
        # Runninng the given script
        executeFile(args[0])
    else:
        # Running the interactive shell
        interactiveShell()
