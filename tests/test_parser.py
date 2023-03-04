from parser import *

def test():

    # basic operations
    print("BASIC OPERATIONS")
    exp = Seq([Declare(Variable('i'), Int(0), Int, False), Declare(Variable('j'), nil(), Int, False), BinOp('=', Variable('i'), BinOp('+', Variable('j'), Int(10))), BinOp('=', Variable('j'), BinOp('+', Variable('j'), Int(1))), Declare(Variable('k'), BinOp('-', Variable('j'), Variable('i')), Int, False)])
    if (parse("int i =0; int j; i = j+10; j = j+1; int k = j-i;") == exp):
        print("passed")
    else:
        print("failed")
        return -1
    print()

    #if-else operations
    print("IF-ELSE")
    exp = Seq( [If( BinOp( '&&',  BinOp( '<',  Variable( 'i'),  Variable( 'j')),  BinOp( '==',  Variable( 'k'),  Int( 10))),  Seq( [PRINT( [Variable( 'i'), Variable( 'j')], ' '), BinOp( '=', Variable( 'k'), BinOp( '+', Variable( 'i'), Variable( 'j')))]), None)])
    if (parse("if (i<j && k == 10){ zout(i,j); k = i+j;}") == exp):
        print("passed")
    else:
        print("failed")
        return -1
    print()

    #while-loop
    print("WHILE-LOOP")
    exp = Seq( [Declare( Variable( 'i'), Int( 0), Int, False), While( BinOp( '<', Variable( 'i'), Int( 10)), Seq( [PRINT( [Variable( 'i')], ' '), BinOp( '=', Variable( 'i'), BinOp( '+', Variable( 'i'), Int( 1)))]))])
    
    if (exp == parse("int i =0; while(i<10){ zout(i); i=i+1;}")):
        print("passed")
    else:
        print("failed")
    print()
    
    #for-loop
    print("FOR-LOOP")
    exp = Seq( [For( Declare( Variable( 'i'), Int( 10), Int, False), BinOp( '>', Variable( 'i'), Int( 5)), Seq( [PRINT( [Variable( 'i')], ' '), BinOp( '=', Variable( 'j'), BinOp( '-', Variable( 'i'), Int( 1))), BinOp( '=', Variable( 'i'), BinOp( '-', Variable( 'i'), Int( 1)))]))])
    if (exp == parse("for(int i = 10; i>5;i = i-1){ zout(i); j = i-1; }")):
        print("passed")
    else:
        print("failed")
    print()

    exp = Seq( [Declare( Variable( 'i'), Int( 0), Int, False), For( nil(), BinOp( '<', Variable( 'i'), Int( 5)), Seq( [PRINT( [Variable( 'i')], ' '), BinOp( '=', Variable( 'i'), BinOp( '+', Variable( 'i'), Int( 1)))]))])
    if (exp == parse("int i =0; for( ;i<5; ){ zout(i); i = i+1; }")):
        print("passed")
    else:
        print("failed")
    print()


if __name__ == "__main__" :
    test_parse()
