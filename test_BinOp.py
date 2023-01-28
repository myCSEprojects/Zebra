# Python program to test the implementation of the BinOp
from sim import *
def test():
    a = Int(1)
    b = Int(20)

    c = 1
    d = 20

    # Checking the BODM operators for the Int class
    if (Int(c * d) != evaluate(BinOp("*", a, b))):
        print("Multiplication failed for the Numbers")
        exit()
    if (Int(c + d) != evaluate(BinOp("+", a, b))):
        print("Addition failed for the Numbers")
        exit()
    if (Int(c - d) != evaluate(BinOp("-", a, b))):
        print("Subtraction failed for the Numbers")
        exit()
    if (Float(c / d) != evaluate(BinOp("/", a, b))):
        print("Basic division failed for the Numbers")
        exit()
    
    if (Bool(False) != evaluate(BinOp("&&", Bool(False), Bool(True)))):
        print("Basic Logical and operator failed")
        exit()

    # Checking for the handling of the zero division error
    try:
        evaluate(BinOp("/", c, 0))
        print(" Zero division error not handled properly")
        exit()
    except:
        pass
        
    print("All Test Cases passed")

if (__name__ == "__main__"):
    test()

