from sim import *

def test() :
#     # test case 1
#     x = Variable('x')
#     y = Variable('y')
#     steps_ = BinOp(Operator(0, "+"), Int(5), Int(2))
#     e11 = BinOp(Operator(0, "-"),x,x)
#     e2 = Loop(x,steps_,e11)
#     exp = Seq([Declare(y, Int(0), Int, False), e2])
#     l = evaluate(exp)
    
#     if l != Bool(False) :
#         print("Loop is failed")
#         exit()

# ##    print("Test case 1 passed")

#      #test case 2
#     steps_ = BinOp(Operator(0, "+"), Int(10), Int(20))
#     e11 = BinOp(Operator(0, "-"),x,x)
#     e2 = Loop(x,steps_,e11)

#     l = evaluate(e2,environment)


#     if l != Bool(False) :
#         print("Loop is failed")
#         exit()

##    print("Test case 2 passed")
    
     #test case 3
    identifier_i = Identifier(0,"i")
    i = Variable('i')

    e1 = BinOp(Operator(0, ">"),i,Int(0))
    e2 = BinOp(Operator(0, "-"),i,Int(1))
    e11 = BinOp(Operator(0, "="),i,e2)

    e22 = While(e1,e11)

    l = evaluate(Seq([Declare(identifier_i, Int(7), Int, False), e22]))

    if l != Bool(False) :
        print("While loop is failed")
        return -1
    print("Test case 1 passed")
     #test case 4
    i = Variable('i')

    e1 = BinOp(Operator(0, "<"),i,Int(10))
    e2 = BinOp(Operator(0, "+"),i,Int(1))
    e11 = BinOp(Operator(0, "="),i,e2)

    e22 = While(e1,e11)

    l = evaluate(Seq([Declare(identifier_i, Int(0), Int, False), e22]))

    if l != Bool(False) :
        print("While loop is failed")
        return -1
    print("Test case 2 passed")

     #test case 5
    identifier_a = Identifier(0,"a")
    a = Variable('a')
    
    e2 = BinOp(Operator(0, "="),a,Int(1))
    e1 = BinOp(Operator(0, "<"),a,Int(5))
    e21 = BinOp(Operator(0, "+"),a,Int(1))
    e11 = BinOp(Operator(0, "="),a,e21)

    l = evaluate(Seq([Declare(identifier_a, nil(), Int, False), e2, While(e1,Seq([PRINT([a],""),e11]))]))
    print()

    print("All test cases passed")
    


if (__name__ == "__main__") :
    test()
