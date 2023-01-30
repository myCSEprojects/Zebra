from sim import *

def test1():
    x = Variable("x")
    if (evaluate(PRINT(Int(10), Int(20))) != None):
        print("Basic evaluation of PRINT failed")
        exit()
    print()

    if (evaluate(PRINT(PRINT(BinOp("*", Int(10), Int(10)),Int(20), " "), PRINT(Int(30),Int(40), " ")))) != None:
        print("Basic evaluation of PRINT failed")
        exit()
    print()

    if (evaluate(PRINT(Int(10), PRINT(Int(30),BinOp("+", Int(10), Int(10)))))) != None:
        print("Basic evaluation of PRINT failed")
        exit()
    print()

    if (evaluate(PRINT(PRINT(Int(50),PRINT(Int(10),Int(20))), PRINT(BinOp("-", Int(10), Int(20)),Int(40))))) != None:
        print("Basic evaluation of PRINT failed")
        exit()
    print()
    print("All test cases passed")

if (__name__ == "__main__"):
    test1()