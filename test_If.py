from sim import *

def test():
    x = Variable("x")
    condition = Let(x, Int(20), BinOp("<", x, Int(10)))
    if (evaluate(If(condition, Int(10), Int(20))) != Int(10)):
        print("Basic evaluation of If failed")
        exit()
    print("All test cases passed")

if (__name__ == "__main__"):
    test()