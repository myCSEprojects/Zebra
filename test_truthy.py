from sim import *

def test1():

    if (Bool.truthy(evaluate(BinOp('-',Int(1),Int(1))))) != Bool(False):
        print("Basic evaluation of truthy failed")
        exit()

    if (Bool.truthy(evaluate(BinOp('+',Int(1),Int(2))))) != Bool(True):
        # print(evaluate(truthy(BinOp('+',Int(1),Int(2)))))
        print("Basic evaluation of truthy failed")
        exit()

    
    if (Bool.truthy(evaluate(str_concat(Str(""), str_concat(Str(""), Str("")))))) != Bool(False):
        print("Basic evaluation of truthy failed")
        exit()
    
    print("All test cases passed")


if (__name__ == "__main__"):
    test1() 