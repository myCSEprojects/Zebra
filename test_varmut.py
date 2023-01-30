from sim import *
def test():
    x = Variable("x")
    if (evaluate(Var(x, BinOp("+", Int(20), Int(10))))!=Int(30)):
        print("Basic evaluation of Var failed")
        exit()

    z=Variable("z")
    if (evaluate(Var(x, Let(z,Int(2),BinOp("*",z,z))))!=Int(4)):
        print("Basic evaluation of Var failed")
        exit()

    if (evaluate(Var(x, If(BinOp("<", Int(20), Int(10)), Int(2), BinOp("+", Int(20), Int(10)))))!=Int(30)):
        print("Basic evaluation of Var failed")
        exit()

    y=Variable("Hello")
    if (evaluate(Var(x, y))!=Variable("Hello")):
        print("Basic evaluation of Var failed")
        if (evaluate(Var(x, BinOp("+", Int(10), Int(10))))!=Int(20)):
            print("Basic evaluation of Var failed")
            exit()

    hgx=Variable("hgx")
    if (evaluate(Var(hgx, none))!=none):
        print("Basic evaluation of Var failed")
        exit()
    print("All test cases passed")

if (__name__ == "__main__"):
    test()