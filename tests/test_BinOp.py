# Python program to test the implementation of the BinOp
from sim import *
def test():
    a = Int(1)
    b = Int(20)

    c = 1
    d = 20

    # Checking the BODM operators for the Int class
    if (Int(c * d) != evaluate(BinOp(Operator(0, "*"), a, b))):
        print("Multiplication failed for the Numbers")
        return -1
    if (Int(c + d) != evaluate(BinOp(Operator(0, "+"), a, b))):
        print("Addition failed for the Numbers")
        return -1
    if (Int(c - d) != evaluate(BinOp(Operator(0, "-"), a, b))):
        print("Subtraction failed for the Numbers")
        return -1
    if (Float(c / d) != evaluate(BinOp(Operator(0, "/"), a, b))):
        print("Basic division failed for the Numbers")
        return -1
    
    if (Bool(False) != evaluate(BinOp(Operator(0, "&&"), Bool(False), Bool(True)))):
        print("Basic Logical and operator failed")
        return -1
    # Checking for the handling of the zero division error
    try:
        evaluate(BinOp(Operator(0, "/"), Int(c), Int(0)))
        print(" Zero division error not handled properly")
        return -1
    except:
        pass
        
    print("All Test Cases passed")
    return 0

if (__name__ == "__main__"):
    test()

