from sim import *

def test():

    print("Strings test cases:")
    a = (str_concat(Str("abc"),Str("xyz")))
    b = str_concat(Str("ppp"),a)
    if (evaluate(str_concat(a,b)).value == "abcxyzpppabcxyz"):
        print("Test 1/3 Passed")
    a= evaluate(a)
    if ( evaluate(Slice(Str("abc"),1,3)).value == "bc") : 
        print("Test 2/3 Passed")
    if (evaluate(BinOp('*',Str('abc'),Int(3)))).value == 'abcabcabc':
        print("Test 3/3 Passed")
        
if (__name__ == "__main__"):
    test()
