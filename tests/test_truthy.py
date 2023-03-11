from sim import *

def test():

    if (Bool.truthy(evaluate(BinOp(Operator(0, "-"),Int(1),Int(1))))) != Bool(False):
        print("Basic evaluation of truthy failed")
        return -1
    if (Bool.truthy(evaluate(BinOp(Operator(0, "+"),Int(1),Int(2))))) != Bool(True):
        # print(evaluate(truthy(BinOp(Operator(0, "+"),Int(1),Int(2)))))
        print("Basic evaluation of truthy failed")
        return -1

    
    if (Bool.truthy(evaluate(str_concat(Str(""), str_concat(Str(""), Str("")))))) != Bool(False):
        print("Basic evaluation of truthy failed")
        return -1
    print("Ho")
    
    print("All test cases passed")
    return 0

if (__name__ == "__main__"):
    test() 