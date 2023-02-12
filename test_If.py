from sim import *

def test():
    x = Variable("x")
    condition = Seq(Declare(x, Int(0), "Int", False), BinOp("<", x, Int(20)))
    if (evaluate(If(condition, Int(10), Int(20))) != Int(10)):
        print("Basic evaluation of If failed")
        exit()
    print("All test cases passed")

if (__name__ == "__main__"):
    test()
