from codegen import *

def test():
    a = Int(1)
    b = Int(20)
    c = 1
    d = 20
    v=VM()
    l=[BinOp("-", a,b),BinOp("+", a,b),BinOp("*", a,b),BinOp("/", a,b),BinOp("//", a,b),BinOp("%", a,b),
        UnOp("-", a),BinOp("<", a,b),BinOp(">", a,b),BinOp("^",a,b)]
    m=[Int(c-d),Int(c+d),Int(c*d),Float(c/d),Int(c//d),Int(c%d),Int(-1*c),Bool(c<d),Bool(c>d),Int(c^d)]
    for i in range(7):
        v.load(codegen(l[i]))
        if(m[i]!=v.execute()):
            print("Test Failed: ", i+1)
            return -1
    print("All BinOp and UnOp tests passed")

    condition = Seq([BinOp("<", Int(5), Int(20))])
    v.load(codegen(If(condition,Int(10), Int(20))))
    if (v.execute() != Int(10)):
        print("Basic evaluation of If failed")
        exit()
    print("tests for if passed")


    v.load(codegen(PRINT([BinOp("+",Int(10),Int(30)),Int(20),Str("Hi")])))
    if (v.execute() != None):
        print("Basic evaluation of PRINT failed")
        exit()
    print("tests for PRINT passed")

    
if (__name__ == "__main__"):
    test()