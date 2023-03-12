from sim import *
from typechecking import typecheck
def test():
    x = Identifier(4, "x")
    if (evaluate(Seq([Declare(x, zList(Int, [Int(1)]),zList, False), list_append(Int(2), x), BinOp(Operator(0, "="),Variable('x'), Variable('x'))]))).elements[1] != Int(2):
        print("Basic evaluation of list_append failed")
        return -1
    if (evaluate(Seq([Declare(x, zList(Int, [Int(1)]),zList, False), list_append(Int(2), x), list_remove(Int(1),x)]))) != Int(2):
        print("Basic evaluation of list_remove failed")
        return -1
    if (evaluate(Seq([Declare(x, zList(Int, [Int(1)]),zList, False), list_append(Int(2), x), list_len(x)]))) != Int(2):
        print("Basic evaluation of list_len failed")
        return -1
    if (evaluate(Seq([Declare(x, zList(Str, [Str("hi")]),zList, False), list_insert(Int(0), Str("hello"),x), list_len(x)]))) != Int(2):
        print("Basic evaluation of list_insert failed")
        return -1
    try:
        ast = Seq([Declare(x, zList(Str, [Str("hi")]),zList, False), list_insert(Int(0), Int(1000),x), list_len(x)])
        typecheck(ast)
        evaluate(ast)
        print("Typechecking of list insert failed")
        return -1
    except:
        print("Caught error")
    print("All test cases passed")
    return 0
if (__name__ == "__main__"):
    test()
