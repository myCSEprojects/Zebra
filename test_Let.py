from sim import *

def test():
    # BinOp implementation should be completed before this test

    # Basic testing
    a = Variable('a')
    x = evaluate(Let(a, BinOp("+", Int(1), Int(2)), BinOp("*", a, Int(3))))
    if (x != Int(9)): 
        print("Basic Testing of the Let failed")
        exit()

    # Testing Lexical Scoping
    b = Int(10)
    exp = Let(a, b, a)

    b = Variable('b')
    eval = evaluate(Let(b, Int(20), exp))
    if (eval != Int(10) ):
        print("Lexical Scoping failed")
        exit()

    # Testing shadowing
    x = evaluate(Let(a, Int(2), Let(a, Int(3), a)))
    if (x == Int(2)):
        print("Shadowing failed")
        exit()

    # Testing parameter type checking(should be of type variable)
    a = 1
    try:
        evaluate(Let(a, Int(1), Int(1)))
        print("Type checking of the parameter failed")
        exit()
    except:
        pass
    
    print("All test cases passed successfully")

if (__name__ == "__main__"):
    test()


