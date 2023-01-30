from sim import *

def test1():
    x = Variable("x")

    if (evaluate(BinOp("=", x, Int(2)))) != Int(2):
        print("Basic evaluation of PRINT failed")
        exit()

    if (evaluate(BinOp("=", x, BinOp("*", Int(3), Int(6))))) != Int(18):
        print("Basic evaluation of PRINT failed")
        exit()
    
    if (evaluate(str_concat(Str("abc"), str_concat(Str("ABC"), Str("XYZ"))))) != Str("abcABCXYZ"):
        print("Basic evaluation of PRINT failed")
        exit()
    
    print("All test cases passed")


if (__name__ == "__main__"):
    test1()