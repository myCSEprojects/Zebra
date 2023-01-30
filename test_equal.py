from sim import *

def test1():
    x = Variable("x")

    if (evaluate(BinOp("=", x, Int(2)))) != Int(2):
        print("Basic evaluation of PRINT failed")
        exit()
    print()

    
    print("All test cases passed")


if (__name__ == "__main__"):
    test1()