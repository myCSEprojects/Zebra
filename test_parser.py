from parser import *




def test_parse():

    #basic operations
    print("BASIC OPERATIONS")
    print(parse("int i =0; int j; i = j+10; j = j+1; int k = j-i;"))
    print()
    
    #if-else operations
    print("IF-ELSE")
    print(parse("if (i<j && k == 10){ zout(i,j); k = i+j;}"))
    print()

    #while-loop
    print("WHILE-LOOP")
    print(parse("int i =0; while(i<10){ zout(i); i=i+1;}"))
    print()
    
    #for-loop
    print("FOR-LOOP")
    print(parse("for(int i = 10; i>5;i = i-1){ zout(i); j = i-1; }"))
    print()
    print(parse("int i =0; for( ;i<5; ){ zout(i); i = i+1; }"))
    print()
    



if __name__ == "__main__" :
    test_parse()
