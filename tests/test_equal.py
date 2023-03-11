from sim import *

def test():
    identifier_x = Identifier(0, "x")
    x = Variable("x")

    if (evaluate(Seq([Declare(identifier_x, nil(), Int, False), BinOp(Operator(0, "="), x, Int(2))])) != Int(2)):
        print("Basic evaluation of equality failed")
        return -1
    if (evaluate(Seq([Declare(identifier_x, nil(), Int, False), BinOp(Operator(0, "="), x, BinOp(Operator(0, "*"), Int(3), Int(6)))]))) != Int(18):
        print("Basic evaluation of equality failed")
        return -1
    
    print("All test cases passed")
    return 0


if (__name__ == "__main__"):
    test()