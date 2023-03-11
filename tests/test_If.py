from sim import *

def test():
    identifier_x = Identifier(0, "x")
    x = Variable("x")
    condition = Seq([Declare(identifier_x, Int(0), "Int", False), BinOp(Operator(0, "<"), x, Int(20))])
    if (evaluate(If(condition, Int(10), Int(20))) != Int(10)):
        print("Basic evaluation of If failed")
        exit()
    print("All test cases passed")

if (__name__ == "__main__"):
    test()
