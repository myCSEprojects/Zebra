import sys
from sim import *
def test():
    identifier_x = Identifier(0,"x")
    x = Variable("x")
    if (evaluate(Seq([Declare(identifier_x, nil(), Int, False), BinOp(Operator(0,"="), x, BinOp(Operator(0,"+"), Int(20), Int(10))), BinOp(Operator(0,"+"),x,Int(1))]))!=Int(31)):
        print("Basic evaluation of Seq failed")
        return -1

    
    if (evaluate(Seq([Declare(identifier_x, nil(), Int, False), BinOp(Operator(0,"="), x, BinOp(Operator(0,"+"), Int(20), Int(10))), BinOp(Operator(0,"="), x, BinOp(Operator(0,"+"), x, Int(1))), PRINT([x], " ")]))!=nil()):
        print("Basic evaluation of Seq failed")
        return -1
        
    try:
        evaluate(Seq([Declare(identifier_x, nil(), Int, False), BinOp(Operator(0,"="), x, BinOp(Operator(0,"+"), Int(20), x)), BinOp(Operator(0,"+"),x,Int(1))]))
        print("Did not catch undefined variable error")
        return -1
    except:
        pass
    print()
    print("All test cases passed")
    return 0

if (__name__ == "__main__"):
    test()