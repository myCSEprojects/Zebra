from sim import *

def test() :
    #test case 1
    x = Variable('x')
    y = Variable('y')
    environment = {'y':Int(0)}
    steps_ = BinOp('+', Int(5), Int(2))
    e11 = BinOp('-',x,x)
    e2 = Loop(x,steps_,e11)

    l = evaluate(e2,environment)


    if l != Bool(False) :
        print("Loop is failed")
        exit()

##    print("Test case 1 passed")

     #test case 2
    steps_ = BinOp('+', Int(10), Int(20))
    e11 = BinOp('-',x,x)
    e2 = Loop(x,steps_,e11)

    l = evaluate(e2,environment)


    if l != Bool(False) :
        print("Loop is failed")
        exit()

##    print("Test case 2 passed")
    
     #test case 3
    i = Variable('i')
    environment = {'i':Int(7)}

    e1 = BinOp('>',i,Int(0))
    e2 = BinOp('-',i,Int(1))
    e11 = BinOp('=',i,e2)

    e22 = While(e1,e11)

    l = evaluate(e22,environment)

    if l != Bool(False) :
        print("While loop is failed")
        exit()
##    print("Test case 3 passed")
     #test case 4
    i = Variable('i')
    environment = {'i':Int(0)}

    e1 = BinOp('<',i,Int(10))
    e2 = BinOp('+',i,Int(1))
    e11 = BinOp('=',i,e2)

    e22 = While(e1,e11)

    l = evaluate(e22,environment)

    if l != Bool(False) :
        print("While loop is failed")
        exit()
##    print("Test case 4 passed")

     #test case 5
    a = Variable('a')
    
    e2 = BinOp('=',a,Int(1))
    e1 = BinOp('<',a,Int(5))
    e21 = BinOp('+',a,Int(1))
    e11 = BinOp('=',a,e21)

    l = evaluate(Seq(e2,While(e1,Seq(PRINT(a,Str("")),e11))))
    # l = evaluate(Seq([e2,While(e1,Seq([PRINT(a,Str("")),e11]))]))
    print()

    print("All test cases passed")
    


if (__name__ == "__main__") :
    test()
