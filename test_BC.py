from codegen import *
from VM import *

def test():
    a = Int(1)
    b = Int(20)
    c = 1
    d = 20
    v=VM()
    l=[BinOp(0, "-", a,b),BinOp(0, "+", a,b),BinOp(0, "*", a,b),BinOp(0, "/", a,b),BinOp(0, "//", a,b),BinOp(0, "%", a,b),
        UnOp(0, "-", a),BinOp(0, "<", a,b),BinOp(0, ">", a,b),BinOp(0, "^",a,b)]
    m=[Int(c-d),Int(c+d),Int(c*d),Float(c/d),Int(c//d),Int(c%d),Int(-1*c),Bool(c<d),Bool(c>d),Int(c^d)]
    for i in range(7):
        v.load(codegen(l[i]))
        if(m[i]!=v.execute()):
            print("Test Failed: ", i+1)
            return -1
    print("All BinOp and UnOp tests passed")

    condition = Seq([BinOp(0, "<", Int(5), Int(20))])
    v.load(codegen(If(0, condition,Int(10), Int(20))))
    if (v.execute() != Int(10)):
        print("Basic evaluation of If failed")
        exit()
    print("tests for if passed")


    v.load(codegen(PRINT(0, [BinOp(0, "+",Int(10),Int(30)),Int(20),Str("Hi")])))
    if (v.execute() != nil()):
        print("Basic evaluation of PRINT failed")
        exit()
    print("tests for PRINT passed")

    
if (__name__ == "__main__"):
    test()