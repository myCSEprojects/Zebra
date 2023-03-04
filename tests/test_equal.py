from sim import *

def test():
    x = Variable("x")

    if (evaluate(Seq([Declare(x, nil(), Int, False), BinOp("=", x, Int(2))])) != Int(2)):
        print("Basic evaluation of PRINT failed")
        return -1

    if (evaluate(Seq([Declare(x, nil(), Int, False), BinOp("=", x, BinOp("*", Int(3), Int(6)))]))) != Int(18):
        print("Basic evaluation of PRINT failed")
        return -1
    
    if (evaluate(str_concat(Str("abc"), str_concat(Str("ABC"), Str("XYZ"))))) != Str("abcABCXYZ"):
        print("Basic evaluation of PRINT failed")
        return -1
    
    print("All test cases passed")
    return 0


if (__name__ == "__main__"):
    test()