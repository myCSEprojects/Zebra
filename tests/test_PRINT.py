from sim import *

def test():
    x = Variable("x")
    if (evaluate(PRINT([Int(10), Int(20)]))) != nil():
        print("Basic evaluation of PRINT failed")
        exit()
    print()

    if (evaluate(PRINT([BinOp(Operator(0, "*"), Int(10), Int(10)),Int(20), Int(30),Int(40)]))) != nil():
        print("Basic evaluation of PRINT failed")
        exit()
    print()

    if (evaluate(PRINT([Int(10), Int(30),BinOp(Operator(0, "+"), Int(10), Int(10))]))) != nil():
        print("Basic evaluation of PRINT failed")
        exit()
    print()

    if (evaluate(PRINT([Int(50),Int(10),Int(20), BinOp(Operator(0, "-"), Int(10), Int(20)),Int(40)]))) != nil():
        print("Basic evaluation of PRINT failed")
        exit()
    print()
    print("All test cases passed")
    return 0

if (__name__ == "__main__"):
    test()