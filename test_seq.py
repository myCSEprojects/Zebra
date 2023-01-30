import sys
from sim import *
def test():
    x = Variable("x")
    if (evaluate(Seq(BinOp("=", x, BinOp("+", Int(20), Int(10))), BinOp("+",x,Int(1))))!=Int(31)):
        print("Basic evaluation of Seq failed")
        exit()

    if (evaluate(Seq(BinOp("=", x, BinOp("+", Int(20), Int(10))), Seq(BinOp("=", x, BinOp("+", x, Int(1))), PRINT(x, Str("")))))!=None):
        print("Basic evaluation of Seq failed")
        exit()
        
    try:
        evaluate(Seq(BinOp("=", x, BinOp("+", Int(20), x)), BinOp("+",x,Int(1))))
        print("Did not catch undefined variable error")
        sys.exit()
    except:
        pass
    print()
    print("All test cases passed")

if (__name__ == "__main__"):
    test()