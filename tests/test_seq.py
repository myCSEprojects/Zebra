import sys
from sim import *
def test():
    x = Variable("x")
    if (evaluate(Seq([Declare(x, nil(), Int, False), BinOp("=", x, BinOp("+", Int(20), Int(10))), BinOp("+",x,Int(1))]))!=Int(31)):
        print("Basic evaluation of Seq failed")
        return -1

    
    if (evaluate(Seq([Declare(x, nil(), Int, False), BinOp("=", x, BinOp("+", Int(20), Int(10))), BinOp("=", x, BinOp("+", x, Int(1))), PRINT([x], " ")]))!=nil()):
        print("Basic evaluation of Seq failed")
        return -1
        
    try:
        evaluate(Seq([Declare(x, nil(), Int, False), BinOp("=", x, BinOp("+", Int(20), x)), BinOp("+",x,Int(1))]))
        print("Did not catch undefined variable error")
        return -1
    except:
        pass
    print()
    print("All test cases passed")
    return 0

if (__name__ == "__main__"):
    test()