from parser import *

def test():

    # basic operations
    print("BASIC OPERATIONS")
    exp = Seq([Declare(Identifier(0, 'i'), Int(0), Int, False), Declare(Identifier(0, 'j'), nil(), Int, False), BinOp(Operator(0, "="), Variable('i'), BinOp(Operator(0, "+"), Variable('j'), Int(10))), BinOp(Operator(0, "="), Variable('j'), BinOp(Operator(0, "+"), Variable('j'), Int(1))), Declare(Identifier(0, 'k'), BinOp(Operator(0, "-"), Variable('j'), Variable('i')), Int, False)])
    if (parse("int i =0; int j; i = j+10; j = j+1; int k = j-i;")[0] == exp):
        print("passed")
    else:
        print("failed")
        return -1
    print()

    #if-else operations
    print("IF-ELSE")
    exp = Seq( [If( BinOp(Operator(0, "&&"),  BinOp(Operator(0, "<"),  Variable( 'i'),  Variable( 'j')),  BinOp(Operator(0, "=="),  Variable( 'k'),  Int( 10))),  Seq( [PRINT( [Variable( 'i'), Variable( 'j')], ' '), BinOp(Operator(0, "="), Variable( 'k'), BinOp(Operator(0, "+"), Variable( 'i'), Variable( 'j')))]), None)])
    if (parse("if (i<j && k == 10){ zout(i,j); k = i+j;}")[0] == exp):
        print("passed")
    else:
        print("failed")
        return -1
    print()

    #while-loop
    print("WHILE-LOOP")
    exp = Seq( [Declare(Identifier(0, 'i'), Int( 0), Int, False), While( BinOp(Operator(0, "<"), Variable( 'i'), Int( 10)), Seq( [PRINT( [Variable( 'i')], ' '), BinOp(Operator(0, "="), Variable( 'i'), BinOp(Operator(0, "+"), Variable( 'i'), Int( 1)))]))])
    
    if (exp == parse("int i =0; while(i<10){ zout(i); i=i+1;}")[0]):
        print("passed")
    else:
        print("failed")
    print()
    
    #for-loop
    print("FOR-LOOP")
    exp = Seq( [For( Declare(Identifier(0, 'i'), Int( 10), Int, False), BinOp(Operator(0, ">"), Variable( 'i'), Int( 5)), Seq( [PRINT( [Variable( 'i')], ' '), BinOp(Operator(0, "="), Variable( 'j'), BinOp(Operator(0, "-"), Variable( 'i'), Int( 1))), BinOp(Operator(0, "="), Variable( 'i'), BinOp(Operator(0, "-"), Variable( 'i'), Int( 1)))]))])
    if (exp == parse("for(int i = 10; i>5;i = i-1){ zout(i); j = i-1; }")[0]):
        print("passed")
    else:
        print("failed")
    print()

    exp = Seq( [Declare(Identifier(0, 'i'), Int( 0), Int, False), For( nil(), BinOp(Operator(0, "<"), Variable( 'i'), Int( 5)), Seq( [PRINT( [Variable( 'i')], ' '), BinOp(Operator(0, "="), Variable( 'i'), BinOp(Operator(0, "+"), Variable( 'i'), Int( 1)))]))])
    if (exp == parse("int i =0; for( ;i<5; ){ zout(i); i = i+1; }")[0]):
        print("passed")
    else:
        print("failed")
    print()


if __name__ == "__main__" :
    test_parse()
