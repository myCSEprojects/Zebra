from typechecking import *

def test():
    te = typecheck(BinOp(Operator(0, "+"), Int(2), Int(3)))
    assert te == Int
    te = typecheck(BinOp(Operator(0, "<"), Int(2), Int(3)))
    assert te == Bool
    try:
        typecheck(BinOp(Operator(0, "+"), BinOp(Operator(0, "*"), Int(2), Int(3)), BinOp(Operator(0, "<"), Int(2), Int(3))))
        print("No error detected")
        return -1
    except:
        print("Error detected")
        pass

    te1 = typecheck(BinOp(Operator(0, ">"), Int(4), Int(2)))
    assert te1 == Bool
    te2 = typecheck(BinOp(Operator(0, "+"), Int(4), Int(2)))
    assert te2 == Int
    te3 = typecheck(BinOp(Operator(0, "-"), Int(4), Int(2)))
    assert te3 == Int
    try:
        typecheck(If(BinOp(Operator(0, ">"), Int(4), Int(2)), BinOp(Operator(0, "+"), Int(4), Int(2)), BinOp(Operator(0, "-"), Int(4), Int(2))))
        print("No error detected")
    except:
        print("Error detected")
        return -1

    print("All testcases passed")
    return 0

if(__name__ == "__main__"):
    test()