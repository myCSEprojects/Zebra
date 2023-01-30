import sys
from sim import *
def test():
    x = Variable("x")
    if (evaluate(Seq(BinOp("=", x, BinOp("+", Int(20), Int(10))), BinOp("+",x,Int(1))))!=Int(31)):
        print("Basic evaluation of Var failed")
        exit()
        
    try:
        evaluate(Seq(BinOp("=", x, BinOp("+", Int(20), x)), BinOp("+",x,Int(1))))
        print("Did not catch undefined variable error")
        sys.exit()
    except:
        pass
    print("All test cases passed")

if (__name__ == "__main__"):
    test()