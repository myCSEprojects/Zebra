from sim import *

def test_fun():
    a = Identifier(0,"a")
    b = Identifier(0,"b")   
    f = Identifier(0,"f")
    g = Identifier(0,"g")
    ss = Scopes()
    
    evaluate(DeclareFun(f,Int,[Int, Int],[a,b], BinOp(Operator(0,"+"),Variable('a'),Variable('b'))),ss)

    e = FunCall(
        f, [Int(1),FunCall(f, [Int(8),Int(45)])]
    )
    
    if (evaluate(e,ss).value == 54):
        print("Passed")

    f_ = FunCall(
        f, [Int(1),e]
    )

    if((evaluate(f_,ss)).value == 55): 
        print("Passed")

    evaluate(DeclareFun(g,Int,[Int, Int],[a,b], BinOp(Operator(0,"*"),Variable('a'),Variable('b'))),ss)

    g_ = FunCall(g, [Int(2),Int(9)])

    if evaluate(g_,ss).value == 18 :
        print("Passed")

test_fun()